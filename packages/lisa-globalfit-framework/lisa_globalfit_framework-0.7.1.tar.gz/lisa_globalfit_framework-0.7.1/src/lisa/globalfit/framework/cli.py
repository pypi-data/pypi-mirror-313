import json
import logging
import shutil
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace
from asyncio import get_event_loop, new_event_loop
from multiprocessing import Process
from pathlib import Path
from sys import exit

from lisa.globalfit.framework.args import (
    add_bus_args,
    add_common_args,
    add_engine_execution_args,
    add_execution_plot_args,
    add_module_execution_args,
    add_modules_execution_args,
    add_pipeline_args,
    add_preprocessing_args,
)
from lisa.globalfit.framework.buses import DefaultEventBus
from lisa.globalfit.framework.catalogs.memory import InMemorySourceCatalog
from lisa.globalfit.framework.catalogs.sqlite import SqliteSourceCatalog
from lisa.globalfit.framework.exceptions import FrameworkError
from lisa.globalfit.framework.mock_engine import Engine, ModulePool
from lisa.globalfit.framework.modules.registry import ModuleRegistry
from lisa.globalfit.framework.modules.stub.preprocessor import StubPreprocessor
from lisa.globalfit.framework.msg.control import (
    ConfigureModule,
    IterateModule,
    ModuleGroupConfiguration,
)
from lisa.globalfit.framework.msg.subjects import channel_configure, create_channel_name
from lisa.globalfit.framework.plot import ModuleExecutionDrawer

logger = logging.getLogger(__name__)


def default_workdir(dir: Path | None) -> Path:
    return dir or Path.cwd()


def get_args() -> Namespace:
    parser = ArgumentParser(
        "LISA GlobalFit Framework CLI",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    add_common_args(parser)
    add_bus_args(parser)
    add_pipeline_args(parser)

    subparsers = parser.add_subparsers(dest="command", required=True)
    add_preprocessing_args(subparsers)
    add_modules_execution_args(subparsers)
    add_module_execution_args(subparsers)
    add_engine_execution_args(subparsers)
    add_execution_plot_args(subparsers)

    return parser.parse_args()


async def cmd_preprocess(args: Namespace):
    preprocessor = StubPreprocessor(args.group_label)
    workdir = default_workdir(args.workdir)
    datafile = workdir / args.input_data
    checkpoint = (
        ModulePool.from_json(workdir / args.input_checkpoint)
        if args.input_checkpoint
        else None
    )
    bus = DefaultEventBus(args.servers)
    await bus.connect()
    # TODO Refactor subject creation with engine code.
    channel = create_channel_name(args.pipeline_run_id, channel_configure("engine"))
    logger.info(f"running {preprocessor.group_label} preprocessor")
    config = preprocessor.preprocess(datafile, checkpoint)
    preprocessor.write_group_configuration(config, args.output_group_configuration_path)

    # TODO If checkpoint is given, subtract signal from other groups to reduce the
    # amount of pre-processing to be done by children modules.
    # For now, the input data file is copied as-is to the preprocessed signal
    # location.
    logger.warning("TODO: group-level subtraction of signals")
    shutil.copy(datafile, args.output_preprocessed_signal)

    await bus.publish(
        channel,
        ModuleGroupConfiguration(
            group=preprocessor.group_label,
            labels=tuple(worker.module_label for worker in config.modules),
        ).encode(),
    )


async def cmd_plot(args: Namespace):
    drawer = ModuleExecutionDrawer()
    drawer.plot_corner(
        chains=args.input_chain,
        dataset=args.chain_location,
        output=Path(args.input_chain).with_suffix(".svg"),
    )


async def cmd_start_module(args: Namespace):
    workdir = default_workdir(args.workdir)
    # TODO Split all stub-related code to dedicated package.
    group = ModulePool.from_group_configuration(
        args.input_group_configuration_path, args.pipeline_run_id
    )
    channel_name = create_channel_name(
        args.pipeline_run_id,
        args.group_label,
        args.module_label,
    )
    module = ModuleRegistry.create(
        name="stub",
        datafile=workdir / args.input_data,
        output_checkpoint=workdir / args.output_checkpoint,
        channel_name=channel_name,
        bus=DefaultEventBus(args.servers),
    )
    iteration_config = IterateModule(
        idx_iteration=args.current_iteration,
        detections=InMemorySourceCatalog(
            detection_map={
                subject: entry.state.log_likelihood
                for subject, entry in group.workers.items()
                if entry.state.log_likelihood.parameters
            }
        ),
        step_count=args.n_steps,
    )
    await module.setup()
    await module.run(
        ConfigureModule(group.workers[channel_name].state), iteration_config
    )


async def cmd_start_all_modules(args: Namespace):
    pool = ModulePool.from_group_configuration(args.input_group_configuration_path)
    pids = [
        Process(
            target=main,
            args=(
                # Forward arguments to module subprocess, overriding the command and
                # setting the corresponding module label.
                Namespace(
                    **{
                        **vars(args),
                        "no_global_loop": True,
                        "command": "start-module",
                        "module_label": module.label,
                        "group_label": module.group,
                        "output_checkpoint": f"checkpoint_{module.label}.h5",
                    }
                ),
            ),
        )
        for module in pool.workers.values()
    ]

    logger.info(f"starting {len(pids)} module subprocesses")
    for pid in pids:
        pid.start()

    for pid in pids:
        pid.join()
        if pid.exitcode != 0:
            raise FrameworkError(f"subprocess {pid} exited with error")


async def cmd_start_engine(args: Namespace):
    with open(args.expected_groups) as f:  #  noqa: ASYNC230
        content = json.load(f)

    engine = Engine(
        expected_groups=[group["label"] for group in content],
        bus=DefaultEventBus(args.servers),
        catalog=SqliteSourceCatalog(args.catalog_db),
        output=args.output_checkpoint,
        pipeline_run_id=args.pipeline_run_id,
        max_iterations=args.max_iterations,
    )
    await engine.setup()
    result = await engine.run(args.current_iteration)
    await engine.write_iteration_decision(result, args.output_iteration_decision)


def main(args: Namespace | None = None):
    args = args or get_args()
    logging.basicConfig(
        level=args.log_level,
        format="%(asctime)s.%(msecs)03d [%(levelname)s] %(name)s %(message)s",
        datefmt=r"%Y-%m-%dT%H:%M:%S",
    )

    cmd_registry = {
        "plot": cmd_plot,
        "preprocess": cmd_preprocess,
        "start-module": cmd_start_module,
        "start-modules": cmd_start_all_modules,
        "start-engine": cmd_start_engine,
    }
    fn = cmd_registry.get(args.command)

    if fn is None:
        logger.error(f"unknown command {args.command}")
        exit(1)

    # When spawning subprocesses, the global event loop is used by default. This raises
    # runtime errors when trying to run tasks because the event loop is already
    # running. To prevent this behaviour, we create a new event loop in this specific
    # case.
    # Note that this is only required for development purposes which rely on the
    # `start-modules` command, but in production containers will be started
    # independently.
    # See https://github.com/python/asyncio/issues/421
    if vars(args).get("no_global_loop", False):
        loop = new_event_loop()
    else:
        loop = get_event_loop()

    task = loop.create_task(fn(args))
    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        # TODO Add two-stages cleanup mechanism, waiting for in-flight tasks to
        # complete, falling back to direct exit on second KeyboardInterrupt.
        logger.info("exiting immediately")
        exit(1)
    except FrameworkError as err:
        logger.error(err)
        exit(1)


if __name__ == "__main__":
    main()
