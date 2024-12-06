import base64
import logging
import time
from typing import Any, Literal, Optional, Union

import httpx
from pydantic import BaseModel, Field, field_validator

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
SORT = {"order": "desc", "column": "startedAt"}


class TechsupportSnapshotSettings(BaseModel):
    snapshot_id: str = "$last"
    backupDb: bool = True
    removeCli: bool = False


class TechsupportPayload(BaseModel):
    databases: bool = False
    systemLogs: bool = True
    discoveryServicesLogs: bool = True
    snapshot: TechsupportSnapshotSettings = TechsupportSnapshotSettings()
    usageData: bool = True


class Job(BaseModel):
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

    # def get_job_by_id(self, job_id: Union[str, int]) -> Optional[Job]:  # TODO: NIM-16050
    #     """Get a job by its ID and returns it as a Job object.
    #
    #     Args:
    #         job_id: ID of the job to retrieve
    #
    #     Returns: Job object if found, None if not found
    #
    #     """
    #     jobs = self.all_jobs.all(filters={"id": ["eq", str(job_id)]}, columns=self.columns)
    #     if not jobs:
    #         return None
    #     return Job(**jobs[0])

    def get_job_by_scheduled_time(self, scheduled_at: Union[str, int]) -> Optional[Job]:
        """Get a job by its scheduled time and returns it as a Job object.

        Args:
            scheduled_at: The time the job was scheduled

        Returns: Job object if found, None if not found

        """
        jobs = self.all_jobs.all(filters={"scheduledAt": ["eq", str(scheduled_at)]}, columns=self.columns)
        if not jobs:
            return None
        return Job(**jobs[0])

    # TODO: 7.0 Change to Job object
    def _return_job_when_done(self, job_filter: dict, retry: int = 5, timeout: int = 5):
        """
        Returns the finished job. Only supports Snapshot related Jobs
        Args:
            job_filter: table filter for jobs
            retry: how many times to query the table
            timeout: how long to wait in-between retries

        Returns:
            job: list[dict[str, str]]: a job that has a status of done
        """
        if "name" not in job_filter and "snapshot" not in job_filter:
            raise SyntaxError("Must provide a Snapshot ID and or name for a filter.")
        time.sleep(1)  # give the IPF server a chance to start the job

        jobs = self.all_jobs.fetch(filters=job_filter, sort=SORT, columns=self.columns)
        logger.debug(f"Job filter: {job_filter}\nList of jobs:{jobs}")
        if jobs:
            # if the job is already completed, we return it
            if jobs[0]["isDone"]:
                return jobs[0]
            # use the start time of this job to identify this specific job
            start_time = jobs[0]["startedAt"]
            job_filter["startedAt"] = ["eq", start_time]
            logger.debug(f"New job_filter: {job_filter}")

            for retries in range(retry):
                job = self.all_jobs.fetch(filters=job_filter, sort=SORT, columns=self.columns)[0]
                logger.debug(f"Current job: {job}")
                if job["isDone"]:
                    return job
                logger.info(f"Retry {retries}/{retry}, waiting {timeout} seconds.")
                time.sleep(timeout)
        else:
            logger.debug(f"Job not found: {job_filter}")
        return None

    def check_snapshot_job(
        self, snapshot_id: str, started: int, action: SNAP_ACTIONS, retry: int = 5, timeout: int = 5
    ):
        """Checks to see if a snapshot load job is completed.

        Args:
            snapshot_id: UUID of a snapshot
            started: Integer time since epoch in milliseconds
            action: Type of job to filter on
            timeout: How long in seconds to wait before retry
            retry: how many retries to use when looking for a job, increase for large downloads

        Returns:
            Job dictionary if load is completed, None if still loading
        """
        j_filter = dict(snapshot=["eq", snapshot_id], name=["eq", SNAP_JOBS[action]], startedAt=["gte", started - 100])
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
        j_filter = dict(snapshot=["eq", snapshot_id], name=["eq", "loadGraphCache"], startedAt=["gte", started - 100])
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

    def generate_techsupport(
        self,
        payload: TechsupportPayload = TechsupportPayload(),
        wait_for_ts: bool = True,
        timeout: int = 60,
        retry: int = 5,
    ) -> Job:
        self.client.post(url="/os/techsupport", data=payload.model_dump_json())
        # Wait for the job to start
        time.sleep(2)
        tech_support_jobs = self.all_jobs.all(filters={"name": ["eq", "techsupport"]}, sort=SORT)

        if not tech_support_jobs:
            raise Exception("No techsupport jobs found.")

        job = tech_support_jobs[0]
        if not wait_for_ts:
            return self.get_job_by_scheduled_time(job["scheduledAt"])
        job = self._return_job_when_done(
            job_filter={"scheduledAt": ["eq", job["scheduledAt"]], "name": ["eq", "techsupport"]},
            retry=retry,
            timeout=timeout,
        )
        return Job(**job)

    def download_techsupport_file(self, job_id: str) -> httpx.Response:
        return self.client.get(f"jobs/{str(job_id)}/download")

    def upload_techsupport_file(
        self,
        upload_username: str = "techsupport",
        upload_password: Optional[str] = None,
        upload_file_timeout: int = 600,
        upload_server: Literal["eu", "us"] = "eu",
        techsupport_bytes: bytes = None,
        techsupport_job_id: str = None,
    ):
        upload_url = f"https://upload.{upload_server.lower()}.ipfabric.io/upload"
        if not upload_password:
            raise ValueError("Upload password is required.")
        if not techsupport_job_id and not techsupport_bytes:
            raise ValueError("Techsupport bytes or Job ID is required.")

        if not techsupport_bytes:
            resp = self.download_techsupport_file(techsupport_job_id)
            if resp.status_code != 200:
                raise httpx.HTTPStatusError(
                    f"Failed to download techsupport file: {resp.status_code}", request=resp.request, response=resp
                )
            techsupport_bytes = resp.content
        base64_credentials = base64.b64encode(f"{upload_username}:{upload_password}".encode("utf-8")).decode("utf-8")

        headers = {
            "Content-Type": "application/x-tar",
            "Accept": "application/json",
            "Authorization": f"Basic {base64_credentials}",
            "Content-Length": str(len(techsupport_bytes)),
        }

        upload_response = httpx.post(
            url=upload_url,
            headers=headers,
            content=techsupport_bytes,
            timeout=upload_file_timeout,
        )

        if upload_response.status_code == 200:
            logger.info("Successfully uploaded techsupport file")
        else:
            logger.error(f"Failed to upload techsupport file. Status code: {upload_response.status_code}")
            logger.error(f"Response content: {upload_response.text}")
            upload_response.raise_for_status()
