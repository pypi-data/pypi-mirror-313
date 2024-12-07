__all__ = ["OdeModel", "OdeModelFromText", "Schedule"]

from abc import abstractmethod
from dataclasses import dataclass
from typing import Literal

from serialite import abstract_serializable, serializable

from .job import Job


@abstract_serializable
class Schedule:
    pass


@abstract_serializable
class OdeModel:
    parameters: dict[str, float]

    def store(self, *, deduplicate: bool = True, include_definition: bool = False) -> Job["OdeModel", None]:
        from . import client

        job = client.create_jobs([self], deduplicate=deduplicate, include_definition=include_definition)
        return job[0]

    @abstractmethod
    def update_parameters(self, parameters: dict[str, float]) -> "OdeModel":
        pass

    @abstractmethod
    def update_schedules(self, schedules: dict[str, Schedule]) -> "OdeModel":
        pass


@serializable
@dataclass(frozen=True)
class OdeModelFromText:
    text: str
    format: Literal["analytic", "kroneckerbio", "mass_action", "reaction", "sbml"]

    def parse(self) -> OdeModel:
        from . import client

        job = client.create_jobs([self])[0]
        client.create_contract(jobs=[job], wait=True)
        return job.output_or_raise()
