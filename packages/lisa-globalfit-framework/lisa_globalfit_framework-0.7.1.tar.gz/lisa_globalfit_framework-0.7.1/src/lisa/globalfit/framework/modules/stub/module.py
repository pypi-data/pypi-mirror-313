import logging
from collections.abc import Callable
from functools import partial

import numpy as np
from emcee import EnsembleSampler, State
from emcee.backends import HDFBackend
from scipy import stats

from lisa.globalfit.framework.exceptions import FrameworkError
from lisa.globalfit.framework.model import (
    MarkovChainSamples,
    ModuleExecutionState,
    ParametricModel,
)
from lisa.globalfit.framework.modules.module import ModuleBase
from lisa.globalfit.framework.modules.registry import ModuleRegistry
from lisa.globalfit.framework.msg.control import ConfigureModule, IterateModule
from lisa.globalfit.framework.msg.data import ModuleState
from lisa.globalfit.framework.signal import NoisyGaussianMixture
from lisa.globalfit.framework.waveform import Waveform, WaveformRegistry

logger = logging.getLogger(__name__)


def log_likelihood(wave: Waveform, sample: np.ndarray, signal: np.ndarray) -> float:
    waveform = wave.evaluate(signal[0], *sample)
    residuals = signal[1] - waveform
    square_err = np.sum(residuals**2)
    return -np.log(square_err)


def log_prob(
    prior_fn: Callable,
    log_likelihood_fn: Callable,
    sample: np.ndarray,
    dataset: NoisyGaussianMixture,
) -> float:
    log_prior = prior_fn(sample)
    log_likelihood = log_likelihood_fn(sample, dataset)
    return log_prior + log_likelihood


@ModuleRegistry.register("stub")
class StubModule(ModuleBase):
    """Placeholder module."""

    DEFAULT_SAMPLER_WALKERS = 5

    def __init__(
        self,
        nwalkers: int = DEFAULT_SAMPLER_WALKERS,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.dataset = NoisyGaussianMixture.read_dataset(self.datafile)
        self.n_walkers = nwalkers
        self.rng = np.random.default_rng()
        self.sampler: EnsembleSampler | None = None
        self.sampler_state: State | None = None
        self.log_prob: Callable | None = None
        self.waveform: Waveform | None = None
        self.configure_message: ConfigureModule | None = None

    async def configure(self, msg: ConfigureModule) -> None:
        # Save configure message to build iteration message.
        self.configure_message = msg

        # Set-up prior.
        prior_key = msg.state.log_prior.name
        try:
            dist = getattr(stats, msg.state.log_prior.name)
            logpdf = getattr(dist, "logpdf")
        except AttributeError:
            logger.error(f"prior '{prior_key}' not in known distributions")
            await self.update_status(ModuleExecutionState.ERROR)
            return

        # Build posterior evaluation function using Bayes theorem.
        self.waveform = WaveformRegistry.create(msg.state.log_likelihood.name)
        log_prior_fn = partial(logpdf, msg.state.log_prior.parameters)
        log_likelihood_fn = partial(log_likelihood, self.waveform)
        self.log_prob = partial(log_prob, log_prior_fn, log_likelihood_fn)

        initial_guess = np.repeat(
            msg.state.chain.waveforms.parameters, self.n_walkers, axis=0
        )
        # TODO Initial state need to be scattered for walkers to be independent. Is
        # this the responsibility of the pre-processing or should we do it here ?
        initial_guess += self.rng.normal(size=initial_guess.shape)
        self.sampler_state = State(coords=initial_guess)

        self.sampler = EnsembleSampler(
            nwalkers=self.n_walkers,
            ndim=initial_guess.shape[-1],
            log_prob_fn=self.log_prob,
        )

    async def iterate(self, control: IterateModule) -> ModuleState:
        if (
            self.dataset is None
            or self.sampler is None
            or self.sampler_state is None
            or self.waveform is None
        ):
            raise FrameworkError("trying to iterate misconfigured module")

        # Subtract other sources from signal.
        module_signal = self.dataset.signal.copy()
        params = await control.detections.get_source_parameters()
        for module_name, model in params.items():
            if module_name == self.channel_name:
                continue

            # TODO Handle waveforms of other module types.
            module_signal[1] -= self.waveform.evaluate(
                module_signal[0], *model.parameters[0]
            )

        # This is awfully slow on shared filesystems, but is only used for integration
        # purposes.
        # See https://github.com/dfm/emcee/issues/393
        backend = HDFBackend(self.output_checkpoint)

        # Re-create the sampler, because we cannot just change the posterior args
        # on-the-fly.
        self.sampler = EnsembleSampler(
            nwalkers=self.sampler.nwalkers,
            ndim=self.sampler.ndim,
            log_prob_fn=self.log_prob,
            args=[module_signal],
            backend=backend,
        )

        # Run MCMC on residual.
        new_state = self.sampler.run_mcmc(
            initial_state=self.sampler_state,
            nsteps=control.step_count,
        )
        if new_state is None:
            msg = f"{self.channel_name} got invalid state {new_state} "
            f"at iteration {self.current_iteration}"
            raise FrameworkError(msg)

        self.sampler_state = new_state
        return self.build_iteration_message()

    def build_iteration_message(self) -> ModuleState:
        if self.sampler is None or self.configure_message is None:
            raise FrameworkError("trying to build step message without sampler state")

        flatlnprob = self.sampler.get_log_prob(flat=True)
        flatchain = self.sampler.get_chain(flat=True)
        if flatlnprob is None or flatchain is None:
            raise FrameworkError("trying to build step message without posterior")

        best_sample_pos = np.argmax(flatlnprob)
        best_sample_prob = flatlnprob[best_sample_pos]
        best_sample = flatchain[best_sample_pos]
        logger.info(
            f"{self.channel_name} iteration {self.current_iteration} best sample: "
            f"{best_sample} logprob: {best_sample_prob}"
        )

        return ModuleState(
            chain=MarkovChainSamples(
                idx_iteration=self.current_iteration,
                idx_step_end=self.current_step,
                waveforms=ParametricModel(
                    name=self.configure_message.state.log_likelihood.name,
                    parameters=np.array([best_sample]),
                ),
            ),
            log_prior=self.configure_message.state.log_prior,
            log_proposal=self.configure_message.state.log_proposal,
            log_likelihood=self.configure_message.state.log_likelihood,
        )
