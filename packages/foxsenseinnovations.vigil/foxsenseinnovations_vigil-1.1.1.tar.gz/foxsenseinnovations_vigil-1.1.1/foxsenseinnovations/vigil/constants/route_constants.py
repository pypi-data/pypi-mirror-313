class RouteConstants:
    """
    Constants representing routes for various monitoring endpoints.
    Attributes:
        API_MONITORING (str): Route for API monitoring endpoint.
        ERROR_MONITORING (str): Route for error monitoring endpoint.
        JOB_START_MONITORING (str): Route for job start monitoring endpoint.
        JOB_END_MONITORING (str): Route for job end monitoring endpoint.
        JOB_FAILED_MONITORING (str): Route for job failure monitoring endpoint.
    """
    API_MONITORING = '/api/v1/api-monitoring'
    ERROR_MONITORING = '/api/v1/exception-management'
    JOB_START_MONITORING = '/api/v1/job/monitor/start'
    JOB_END_MONITORING = '/api/v1/job/monitor/end'
    JOB_FAILED_MONITORING = '/api/v1/job/monitor/failed'
