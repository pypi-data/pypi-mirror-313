from typing import Optional
from datetime import date

class StartJob:
    """
    Represents the start event of a job.
    """
    def __init__(
        self,
        jobId: Optional[str] = None,
        jobSlug: Optional[str] = None,
        clientVersion: Optional[str] = None,
        startMessage: Optional[str] = None,
        startTime: Optional[date] = None,
    ):
        """
        Initialize StartJob instance.

        Parameters:
        - job_id (str): Identifier of the Job.
        - job_slug (Optional[str]): Slug of the Job.
        - client_version (Optional[str]): App Version of the client application.
        - start_message (Optional[str]): Custom message describing the job start event.
        - start_time (Optional[Date]): Timestamp at which the job started.
        """
        self.clientVersion = clientVersion
        self.jobId = jobId
        self.jobSlug = jobSlug
        self.startMessage = startMessage
        self.startTime = startTime

class StopJob:
    """
    Represents the stop event of a job.
    """
    def __init__(
        self,
        jobId: Optional[str] = None,
        jobSlug: Optional[str] = None,
        clientVersion: Optional[str] = None,
        stopMessage: Optional[str] = None,
        stopTime: Optional[date] = None,
    ):
        """
        Initialize StopJob instance.

        Parameters:
        - job_id (str): Identifier of the Job.
        - job_slug (Optional[str]): Slug of the Job.
        - client_version (Optional[str]): App Version of the client application.
        - stop_message (Optional[str]): Custom message describing the job stop/failed event.
        - stop_time (Optional[Date]): Timestamp at which the job completed (successfully or failed).
        """
        self.clientVersion = clientVersion
        self.jobId = jobId
        self.jobSlug = jobSlug
        self.stopMessage = stopMessage
        self.stopTime = stopTime

class JobDetail:
    """
    Represents details of a job event.
    """
    def __init__(
        self,
        job_id: Optional[str] = None,
        job_slug: Optional[str] = None,
        client_version: Optional[str] = None,
        message: Optional[str] = None,
        event_time: Optional[date] = None,
    ):
        """
        Initialize JobDetail instance.

        Parameters:
        - job_id (Optional[str]): Identifier of the Job.
        - job_slug (Optional[str]): Slug of the Job.
        - client_version (Optional[str]): App Version of the client application.
        - message (Optional[str]): Custom message describing the job start/stop/failed event.
        - event_time (Optional[Date]): Timestamp at which the job start, completion, or failure occurred.

         Raises:
        - ValueError: If neither job_id nor job_slug is provided.
        """
        self.client_version = client_version
        self.job_id = job_id
        self.job_slug = job_slug
        self.message = message
        self.event_time = event_time
