__all__ = ["OdePosteriorSampleConfiguration"]

from dataclasses import dataclass
from typing import Literal

from serialite import serializable


@serializable
@dataclass(frozen=True)
class OdePosteriorSampleConfiguration:
    """Configuration settings for parameter posterior sampling.

    Attributes
    ----------
    method: `str`, default="NUTS"
        Algorithm to use for the posterior sampling. The possible methods are
        the following pymc.sample step methods:  NUTS ("No U-Turn Sampler"),
        HamiltonianMC, Metropolis, DEMetropolisZ, and Slice.
    tune: `int`, default=1000
        Number of iterations for method-specific algorithm parameter tuning.
    thin: `int`, default=1
        Out of `n` * `thin` raw samples drawn, every `thin` samples are re-
        tained for the final output table.  Can be used to reduce auto-
        correlation among samples.
    """

    method: Literal["NUTS", "HamiltonianMC", "Metropolis", "DEMetropolisZ", "Slice"] = "NUTS"
    tune: int = 1000
    thin: int = 1
