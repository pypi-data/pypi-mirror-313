__all__ = [
    "SmoothedLogUniformDistribution",
    "SmoothedLogUniformPrediction",
    "SmoothedLogUniformResidual",
]

from dataclasses import dataclass

from serialite import serializable

from ...expression import StaticExpression, Unit
from .base import Distribution, DistributionPrediction, DistributionResidual


@serializable
@dataclass(frozen=True, kw_only=True, slots=True)
class SmoothedLogUniformDistribution(Distribution):
    time: StaticExpression
    target: str
    lower: StaticExpression
    upper: StaticExpression
    logspace_smoothness: StaticExpression | None = None


@serializable
@dataclass(frozen=True, kw_only=True, slots=True)
class SmoothedLogUniformPrediction(DistributionPrediction):
    time: float
    time_unit: Unit
    target: str
    unit: Unit
    prediction: float


@serializable
@dataclass(frozen=True, kw_only=True, slots=True)
class SmoothedLogUniformResidual(DistributionResidual):
    time: float
    time_unit: Unit
    target: str
    measurement: float
    unit: Unit
    prediction: float
    residual: float
    normalized_residual: float
    log_likelihood: float
