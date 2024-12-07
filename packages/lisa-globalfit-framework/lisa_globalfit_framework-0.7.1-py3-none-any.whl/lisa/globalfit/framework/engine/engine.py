import asyncio
import logging
import traceback
from asyncio import Event, Future, Task
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass

from lisa.globalfit.framework.bus import AckMessage, PullEventBus, PullSubscriber
from lisa.globalfit.framework.engine.rule import Response, Rule, RuleIdentifier
from lisa.globalfit.framework.msg.streams import STREAM_INFRA

logger = logging.getLogger(__name__)


@dataclass
class RuleEvent:
    msg: AckMessage
    rule: Rule


@dataclass
class RuleSubscription:
    rule: Rule
    sub: PullSubscriber

    async def get_next_event(self) -> RuleEvent:
        msg = await self.sub.fetch_message()
        return RuleEvent(msg, self.rule)


class Engine:
    CONSUMER_NAME = "rule-engine"

    def __init__(self, bus: PullEventBus) -> None:
        self.bus = bus
        self.rules: dict[RuleIdentifier, RuleSubscription] = {}
        self.wake = Event()
        self.should_stop = Event()
        self.executor = ProcessPoolExecutor()
        self.internal_tasks: tuple[Task, ...] = ()
        self.running_tasks: dict[Future, RuleEvent] = {}
        self.running_tasks_ids: set[str] = set()

    async def setup(self) -> None:
        await self.bus.connect()
        await self.bus.add_stream(STREAM_INFRA)

    async def register_rules(self, rules: list[Rule]) -> None:
        await asyncio.gather(*(self.register_rule(r) for r in rules))

    async def register_rule(self, rule: Rule) -> None:
        if rule.id in self.rules:
            raise ValueError(f"trying to register duplicate rule {rule.id!r}")

        # TODO Move subject checking logic to dedicated stream method.
        rule_prefix = f"{STREAM_INFRA.name}."
        if not rule.subject.startswith(rule_prefix):
            raise ValueError(f"rule subject should start with {rule_prefix!r}")

        # Create one durable consumer for each rule, so that messages for a same
        # subject are delivered to all rules attached to it.
        sub = await self.bus.subscribe(rule.subject, rule.id)
        self.rules[rule.id] = RuleSubscription(rule=rule, sub=sub)
        logger.info(f"loaded rule {rule.id!r}")

    async def run(self) -> None:
        logger.info("starting rule engine")
        self.internal_tasks = (
            asyncio.create_task(self.schedule_rule_evaluations()),
            asyncio.create_task(self.handle_rule_evaluation_results()),
        )
        await asyncio.wait(self.internal_tasks, return_when=asyncio.ALL_COMPLETED)

    async def schedule_rule_evaluations(self) -> None:
        while not self.should_stop.is_set():
            event = await self.get_next_event()
            await self.run_handler(event)

    async def handle_rule_evaluation_results(self) -> None:
        while not self.should_stop.is_set():
            if not self.running_tasks:
                logger.debug("waiting for next event")
                # Relying on a wake event is necessary because we can't wait on an
                # empty list of coroutines.
                await self.wake.wait()

            self.wake.clear()
            logger.debug(f"waiting for {len(self.running_tasks)} pending tasks")
            done, _ = await asyncio.wait(
                self.running_tasks.keys(), return_when=asyncio.FIRST_COMPLETED
            )
            await self.handle_results(done)

    async def get_next_event(self) -> RuleEvent:
        tasks = tuple(Task(rule.get_next_event()) for rule in self.rules.values())
        event, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        return next(iter(event)).result()

    async def handle_results(self, tasks: set[Future]) -> None:
        await asyncio.gather(*(self.handle_result(result) for result in tasks))

    async def handle_result(self, task: Future[list[Response]]) -> None:
        event = self.running_tasks[task]
        del self.running_tasks[task]
        self.running_tasks_ids.remove(event.rule.id)
        error = task.exception()
        if error is not None:
            logger.error(f"got exception for task {event.rule.id!r}")
            traceback.print_exception(error)
            # TODO We might want to allow retries of rule evaluations which fail
            # because of transient errrors.
            await event.msg.discard()
            return

        await event.msg.in_progress()
        responses = task.result()
        if responses:
            await self.publish_responses(responses)
        await event.msg.ack()

    async def publish_responses(self, responses: list[Response]) -> None:
        await asyncio.gather(
            *(self.publish_response(response) for response in responses)
        )

    async def publish_response(self, response: Response) -> None:
        await self.bus.publish(response.subject, response.msg.encode())

    async def run_handler(self, event: RuleEvent) -> None:
        if not event.rule.is_active:
            logger.debug(f"skipping evaluation of inactive rule {event.rule.id!r}")
            await event.msg.discard()
            return

        if event.rule.id in self.running_tasks_ids:
            logger.debug(f"scheduling re-delivery of busy rule {event.rule.id!r}")
            await event.msg.nack()
            return

        logger.debug(f"scheduling evaluation of rule {event.rule.id!r}")
        loop = asyncio.get_event_loop()
        task = loop.run_in_executor(
            self.executor, event.rule.evaluate, event.msg.subject, event.msg.data
        )
        self.running_tasks[task] = event
        self.running_tasks_ids.add(event.rule.id)
        await event.msg.in_progress()
        self.wake.set()

    async def shutdown(self) -> None:
        logger.info("shutting down engine")
        self.should_stop.set()
        for task in self.internal_tasks:
            if not task.done():
                task.cancel()
        await asyncio.wait(self.internal_tasks, return_when=asyncio.ALL_COMPLETED)
        await self.bus.close()
        self.executor.shutdown()
