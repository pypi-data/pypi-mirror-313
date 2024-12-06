from typing import Optional, List, Dict, Any
from datetime import datetime

class ExcludeOptions:
    """
    Represents options for excluding certain types of requests from monitoring.
    Attributes:
        GET: List of endpoints to exclude from GET requests.
        POST: List of endpoints to exclude from POST requests.
        PATCH: List of endpoints to exclude from PATCH requests.
        PUT: List of endpoints to exclude from PUT requests.
        DELETE: List of endpoints to exclude from DELETE requests.
    """
    def __init__(self, GET: Optional[List[str]] = None, POST: Optional[List[str]] = None,
                 PATCH: Optional[List[str]] = None, PUT: Optional[List[str]] = None,
                 DELETE: Optional[List[str]] = None) -> None:
        self.GET = GET or []
        self.POST = POST or []
        self.PATCH = PATCH or []
        self.PUT = PUT or []
        self.DELETE = DELETE or []

class RequestDetails:
    """
    Represents details of an HTTP request.
    Attributes:
        headers: Dictionary containing request headers.
        userAgent: User agent string indicating the client's browser or application.
        cookies: Dictionary containing request cookies.
        ip: IP address of the client.
        requestBody: Dictionary containing the request body.
        protocol: Protocol used for the request (e.g., HTTP, HTTPS).
        hostName: Hostname of the server.
        query: Dictionary containing query parameters.
        subdomains: List of subdomains in the request.
        uaVersionBrand: Version and brand information from the user agent.
        uaMobile: Mobile information from the user agent.
        uaPlatform: Platform information from the user agent.
        reqAcceptEncoding: Accept encoding header from the request.
        reqAcceptLanguage: Accept language header from the request.
        rawHeaders: List of raw headers from the request.
        remoteAddress: IP address of the client.
        remoteFamily: Family of the IP address (e.g., IPv4, IPv6).
        path: Path of the requested resource.
        params: Additional parameters of the request.
    """
    def __init__(self, headers: Optional[Dict[str, Any]] = None, userAgent: Optional[str] = None,
                 cookies: Optional[Dict[str, Any]] = None, ip: Optional[str] = None,
                 requestBody: Optional[Dict[str, Any]] = None, protocol: Optional[str] = None,
                 hostName: Optional[str] = None, query: Optional[Dict[str, Any]] = None,
                 subdomains: Optional[List[str]] = None, uaVersionBrand: Optional[str] = None,
                 uaMobile: Optional[str] = None, uaPlatform: Optional[str] = None,
                 reqAcceptEncoding: Optional[str] = None, reqAcceptLanguage: Optional[str] = None,
                 rawHeaders: Optional[List[str]] = None, remoteAddress: Optional[str] = None,
                 remoteFamily: Optional[str] = None, path: Optional[str] = None,
                 params: Optional[str] = None) -> None:
        self.headers = headers or {}
        self.userAgent = userAgent
        self.cookies = cookies or {}
        self.ip = ip
        self.requestBody = requestBody or {}
        self.protocol = protocol
        self.hostName = hostName
        self.query = query or {}
        self.subdomains = subdomains or []
        self.uaVersionBrand = uaVersionBrand
        self.uaMobile = uaMobile
        self.uaPlatform = uaPlatform
        self.reqAcceptEncoding = reqAcceptEncoding
        self.reqAcceptLanguage = reqAcceptLanguage
        self.rawHeaders = rawHeaders or []
        self.remoteAddress = remoteAddress
        self.remoteFamily = remoteFamily
        self.path = path
        self.params = params

class ApiRequest:
    """
    Represents an API request.
    Attributes:
        httpMethod: HTTP method of the request (e.g., GET, POST).
        url: URL of the request.
        originalUrl: Original URL of the request.
        baseUrl: Base URL of the request.
        httpVersion: HTTP version of the request.
        request_details: Details of the request (an instance of RequestDetails).
        host: Host of the request.
    """
    def __init__(self, httpMethod: str, url: str, originalUrl: str, baseUrl: str,
                 httpVersion: int, request_details: RequestDetails, host: Optional[str] = None) -> None:
        self.host = host
        self.httpMethod = httpMethod
        self.url = url
        self.originalUrl = originalUrl
        self.baseUrl = baseUrl
        self.httpVersion = httpVersion
        self.request_details = request_details.__dict__

class ApiResponse:
    """
    Represents an API response.
    Attributes:
        responseStatusCode: HTTP status code of the response.
        responseStatusMessage: Status message of the response.
        responseBody: Dictionary containing the response body.
        responseHeaders: Dictionary containing response headers.
    """
    def __init__(self, responseStatusCode: int, responseStatusMessage: str,
                 responseBody: Optional[Dict[str, Any]] = None, responseHeaders: Optional[Dict[str, Any]] = None) -> None:
        self.responseStatusCode = responseStatusCode
        self.responseStatusMessage = responseStatusMessage
        self.responseBody = responseBody or {}
        self.responseHeaders = responseHeaders or {}

class ApiMonitoringRecord:
    """
    Represents a record of API monitoring.
    Attributes:
        startTime: Start time of the monitoring record.
        endTime: End time of the monitoring record.
        request: API request (an instance of ApiRequest).
        response: API response (an instance of ApiResponse).
        clientVersion: Version of the client making the request.
    """
    def __init__(
      self, startTime: datetime, endTime: datetime, request: ApiRequest, response: ApiResponse,
                 clientVersion: Optional[str] = None) -> None:
        self.clientVersion = clientVersion
        self.startTime = startTime
        self.endTime = endTime
        self.request = request
        self.response = response

class ApiMonitoringOptions:
    """
    Represents options for API monitoring.
    Attributes:
        exclude: Options for excluding certain types of requests from monitoring (an instance of ExcludeOptions).
        clientVersion: Version of the client to monitor.
    """
    def __init__(self, exclude: Optional[ExcludeOptions] = None, clientVersion: Optional[str] = None) -> None:
        self.exclude = exclude or ExcludeOptions()
        self.clientVersion = clientVersion
