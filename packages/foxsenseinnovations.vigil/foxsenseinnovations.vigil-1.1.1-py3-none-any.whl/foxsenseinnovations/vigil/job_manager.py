from datetime import datetime, timezone
from foxsenseinnovations.vigil.vigil_types.job_monitoring_types import JobDetail, StartJob, StopJob
from foxsenseinnovations.vigil.api_service import ApiService
from foxsenseinnovations.vigil.constants.route_constants import RouteConstants
from foxsenseinnovations.vigil.vigil import Vigil
from typing import Any
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
class JobMonitoring(Vigil):
    """
    JobMonitoring class provides methods to capture job events and send data to the Vigil API for monitoring
    and analysis.
    """
    def capture_job_start(self, job_detail: JobDetail) -> str:
        """
        Capture the start of a job and send the data to Vigil for monitoring.
        Args:
            job_detail (JobDetail): Details of the job to be started.
        Returns:
            str: A message indicating the success or failure of the operation.
        """
        start_job_request = StartJob(
            clientVersion=job_detail.client_version if job_detail.client_version is not None else Vigil.version,
            jobId=job_detail.job_id if job_detail.job_id is not None else None,
            jobSlug=job_detail.job_slug if job_detail.job_slug is not None else None,
            startMessage=job_detail.message,
            startTime=job_detail.event_time if job_detail.event_time is not None else datetime.now(timezone.utc).isoformat()
        )
        return self._make_api_call(
            RouteConstants.JOB_START_MONITORING,
            start_job_request
        )

    def capture_job_end(self, job_detail: JobDetail) -> str:
        """
        Capture the end of a job and send the data to Vigil for monitoring.
        Args:
            job_detail (JobDetail): Details of the job that has ended.
        Returns:
            str: A message indicating the success or failure of the operation.
        """
        stop_job_request = StopJob(
            clientVersion=job_detail.client_version if job_detail.client_version is not None else Vigil.version,
            jobId=job_detail.job_id if job_detail.job_id is not None else None,
            jobSlug=job_detail.job_slug if job_detail.job_slug is not None else None,
            stopMessage=job_detail.message,
            stopTime=job_detail.event_time if job_detail.event_time is not None else datetime.now(timezone.utc).isoformat()
        )
        return self._make_api_call(
            RouteConstants.JOB_END_MONITORING,
            stop_job_request
        )

    def capture_job_failure(self, job_detail: JobDetail) -> str:
        """
        Capture the failure of a job and send the data to Vigil for monitoring.
        Args:
            job_detail (JobDetail): Details of the job that has failed.
        Returns:
            str: A message indicating the success or failure of the operation.
        """
        failed_job_request = StopJob(
            clientVersion=job_detail.client_version if job_detail.client_version is not None else Vigil.version,
            jobId=job_detail.job_id if job_detail.job_id is not None else None,
            jobSlug=job_detail.job_slug if job_detail.job_slug is not None else None,
            stopMessage=job_detail.message,
            stopTime=job_detail.event_time if job_detail.event_time is not None else datetime.now(timezone.utc).isoformat()
        )
        return self._make_api_call(
            RouteConstants.JOB_FAILED_MONITORING,
            failed_job_request
        )

    def _make_api_call(self, route: str, data: Any) -> str:
        """
        Make an API call to Vigil.
        Args:
            route (str): The route of the API to call.
            data (Any): The data to send in the API call.
        Returns:
            str: A message indicating the success or failure of the API call.
        """
        try:
            if isinstance(data, (StartJob, StopJob, JobDetail)):
                data = data.__dict__
            ApiService.make_api_call(
                Vigil.instance_url,
                route,
                data,
                Vigil.api_key
            )
            logging.info(f'[Vigil] Job event has been logged successfully for route: {route}')
            return f'[Vigil] Job event has been logged successfully for route: {route}'
        except Exception as e:
            error_message = f'[Vigil] Error while creating job record for route {route} :: {str(e)}'
            logging.error(error_message)


JobManager = JobMonitoring()
