from __future__ import annotations

__all__ = ["Job", "JobDescriptor"]

from dataclasses import dataclass
from typing import Generic, TypeVar

from serialite import Serializer

from .dataclass_helpers import ignore_extra_kwargs
from .progress import DisplayJobProgress
from .status import Status

JobDefinition = TypeVar("JobDefinition", bound=Serializer)
JobOutput = TypeVar("JobOutput", bound=Serializer)


@dataclass(frozen=True, kw_only=True, slots=True)
class JobDescriptor(Generic[JobDefinition, JobOutput]):
    definition: type[JobDefinition]
    display_job_progress: type[DisplayJobProgress] = DisplayJobProgress
    output: type[JobOutput]


@ignore_extra_kwargs
@dataclass(frozen=True, kw_only=True, slots=True)
class Job(Generic[JobDefinition, JobOutput]):
    id: str
    status: Status
    task_name: str

    created_at: str
    started_at: str | None = None
    finished_at: str | None = None

    definition: JobDefinition | None = None
    exception: dict | None = None
    output: JobOutput | None = None

    @staticmethod
    def from_id(
        id: str,
        include_definition: bool = False,
        include_output: bool = False,
    ) -> Job[JobDefinition, JobOutput]:
        from . import client

        params = {"include_definition": include_definition, "include_output": include_output}
        response = client.httpx_client.get(f"/jobs/{id}/", params=params).json()
        job = Job(**response)

        if include_definition:
            descriptor = client.job_descriptors[job.task_name]
            definition = descriptor.definition.from_data(job.definition).or_die()
            object.__setattr__(job, "definition", definition)

        if include_output and job.status == Status.succeeded:
            descriptor = client.job_descriptors[job.task_name]
            output = descriptor.output.from_data(job.output).or_die()
            object.__setattr__(job, "output", output)

        return job

    def refresh(
        self,
        force: bool = False,
        include_definition: bool = False,
        include_output: bool = False,
    ) -> Job[JobDefinition, JobOutput]:
        if (
            force
            or (include_definition and self.definition is None)
            or (include_output and self.output is None)
            or self.status == Status.submitted
        ):
            return Job.from_id(id=self.id, include_definition=include_definition, include_output=include_output)
        else:
            return self

    def output_or_raise(self) -> JobOutput:
        job = self.refresh(include_output=True)
        job.raise_if_error()
        return job.output

    def raise_if_error(self) -> None:
        job = self.refresh()
        if job.status != Status.failed:
            return
        exception_type = job.exception["_type"]
        exception_message = job.exception["message"]
        raise type(exception_type, (Exception,), {})(exception_message)

    def progress(self) -> list:
        from . import client

        params = {"limit": 100, "offset": 0}
        progress = []
        while True:
            response = client.httpx_client.get(f"/jobs/{self.id}/progress/", params=params).json()
            progress.extend(response)
            if len(response) < params["limit"]:
                break
            params["offset"] += params["limit"]
        return progress
