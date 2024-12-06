import logging
from time import sleep
from typing import Any, Literal, Optional, Union

from pydantic import BaseModel, Field, field_validator, ConfigDict

from .table import BaseTable

logger = logging.getLogger("ipfabric")

SNAP_JOBS = {
    "load": "snapshotLoad",
    "unload": "snapshotUnload",
    "download": "snapshotDownload",
    "add": "discoveryAdd",
    "refresh": "discoveryRefresh",
    "delete": "deleteDevice",
    "recalculate": "recalculateSites",
    "new": "discoveryNew",
}

SNAP_ACTIONS = Literal["load", "unload", "download", "add", "refresh", "delete", "discoveryNew"]


class Job(BaseModel):
    model_config = ConfigDict(extra="allow")
    finishedAt: Optional[int] = None
    snapshot: Optional[str] = None
    name: Optional[str] = None
    id: Optional[str] = None
    username: Optional[str] = None
    isDone: bool = False
    scheduledAt: Optional[int] = None
    downloadFile: Optional[str] = None
    startedAt: Optional[int] = None
    status: Optional[str] = None

    @field_validator("snapshot")
    @classmethod
    def _empty_str_to_none(cls, v: Union[None, str]) -> Union[None, str]:
        return v if v else None


class Jobs(BaseModel):
    client: Any = Field(exclude=True)

    @property
    def all_jobs(self):
        return BaseTable(client=self.client, endpoint="tables/jobs")

    @property
    def columns(self):
        return [
            "id",
            "downloadFile",
            "finishedAt",
            "isDone",
            "name",
            "scheduledAt",
            "snapshot",
            "startedAt",
            "status",
            "username",
        ]

    def get_job_by_id(self, job_id: Union[str, int]) -> Optional[Job]:
        """Get a job by its ID and returns it as a Job object.

        Args:
            job_id: ID of the job to retrieve

        Returns: Job object if found, None if not found

        """
        jobs = self.all_jobs.all(filters={"id": ["eq", str(job_id)]}, columns=self.columns)
        if not jobs:
            return None
        return Job(**jobs[0])

    def _return_job(self, job_filter: dict) -> Union[Job, None]:
        """Returns the job. Only supports Snapshot related Jobs.

        Args:
            job_filter: table filter for jobs

        Returns:
            job: Job: Object about the job
        """
        if "name" not in job_filter and "snapshot" not in job_filter:
            raise SyntaxError("Must provide a Snapshot ID and name for a filter.")
        sleep(5)  # give the IPF server a chance to start the job
        # find the running snapshotDownload job (i.e. not done)
        jobs = self.all_jobs.fetch(
            filters=job_filter,
            sort={"order": "desc", "column": "startedAt"},
            columns=self.columns,
        )
        logger.debug(f"Job filter: {job_filter}\nlist of jobs:{jobs}")
        if not jobs:
            logger.warning(f"Job not found: {job_filter}")
            return None

        return Job(**jobs[0])

    def _return_job_when_done(self, job_filter: dict, retry: int = 5, timeout: int = 5) -> Union[Job, None]:
        """
        Returns the finished job. Only supports Snapshot related Jobs
        Args:
            job_filter: table filter for jobs
            retry: how many times to query the table
            timeout: how long to wait in-between retries

        Returns:
            job: Job: Object about the job
        """
        job = self._return_job(job_filter)

        if not job or job.isDone:
            return job

        for retries in range(retry):
            job = self.get_job_by_id(job.id)
            if job.isDone:
                return job
            sleep(timeout)

        return None

    def check_snapshot_job(
        self, snapshot_id: str, started: int, action: SNAP_ACTIONS, retry: int = 5, timeout: int = 5
    ) -> Union[Job, None]:
        """Checks to see if a snapshot load job is completed.

        Args:
            snapshot_id: UUID of a snapshot
            started: Integer time since epoch in milliseconds
            action: Type of job to filter on
            timeout: How long in seconds to wait before retry
            retry: how many retries to use when looking for a job, increase for large downloads

        Returns:
            Job: Job object or None if did not complete.
        """
        j_filter = dict(snapshot=["eq", snapshot_id], name=["eq", SNAP_JOBS[action]], startedAt=["gte", started - 1000])
        return self._return_job_when_done(j_filter, retry=retry, timeout=timeout)

    def check_snapshot_assurance_jobs(
        self, snapshot_id: str, assurance_settings: dict, started: int, retry: int = 5, timeout: int = 5
    ):
        """Checks to see if a snapshot Assurance Engine calculation jobs are completed.

        Args:
            snapshot_id: UUID of a snapshot
            assurance_settings: Dictionary from Snapshot.get_assurance_engine_settings
            started: Integer time since epoch in milliseconds
            timeout: How long in seconds to wait before retry
            retry: how many retries to use when looking for a job, increase for large downloads

        Returns:
            True if load is completed, False if still loading
        """
        j_filter = dict(snapshot=["eq", snapshot_id], name=["eq", "loadGraphCache"], startedAt=["gte", started - 1000])
        if (
            assurance_settings["disabled_graph_cache"] is False
            and self._return_job_when_done(j_filter, retry=retry, timeout=timeout) is None
        ):
            logger.error("Graph Cache did not finish loading; Snapshot is not fully loaded yet.")
            return False
        j_filter["name"] = ["eq", "saveHistoricalData"]
        if (
            assurance_settings["disabled_historical_data"] is False
            and self._return_job_when_done(j_filter, retry=retry, timeout=timeout) is None
        ):
            logger.error("Historical Data did not finish loading; Snapshot is not fully loaded yet.")
            return False
        j_filter["name"] = ["eq", "report"]
        if (
            assurance_settings["disabled_intent_verification"] is False
            and self._return_job_when_done(j_filter, retry=retry, timeout=timeout) is None
        ):
            logger.error("Intent Calculations did not finish loading; Snapshot is not fully loaded yet.")
            return False
        return True
