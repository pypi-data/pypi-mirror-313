from typing import Any, Dict, Optional
from django.http import QueryDict
from django.urls import resolve
from foxsenseinnovations.vigil.vigil_types.api_monitoring_types import ApiRequest, ApiResponse, ExcludeOptions, RequestDetails
from foxsenseinnovations.vigil.enums.http_method_enum import HttpMethod
from foxsenseinnovations.vigil.vigil_utils.common_utils import MaskOptions, mask_data, generate_path
import json
import base64
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
def serialize_file(file):
    """
    Serialize file data for API consumption.
    Args:
        file: The file object to serialize.
    Returns:
        Dict[str, Any]: The serialized file data.
    """
    file_content = file.read()
    try:
        file_content = file_content.decode('utf-8')
    except UnicodeDecodeError:
        file_content = base64.b64encode(file_content).decode('utf-8')
    return {
        'filename': file.name,
        'content': file_content,
    }

def parse_multipart_body(request):
    """
    Parse multipart request body and extract data.
    Args:
        request: The HTTP request object.
    Returns:
        Dict[str, Any]: Parsed data from the request body.
    """
    data = dict(request.POST)
    files_data = {key: serialize_file(file) for key, file in request.FILES.items()}
    data.update(files_data)
    return data

def is_empty(request):
    """
    Check if an HTTP request is empty (contains no body, POST data, or files).
    Args:
        request: The HTTP request object.
    Returns:
        bool: True if the request is empty, False otherwise.
    """
    if (not request.body) and len(request.POST)==0 and len(request.FILES)==0:
        return True
    else:
        return False

def extract_path_params(request):
    """
    Extract path parameters from an HTTP request.
    Args:
        request: The HTTP request object.
    Returns:
        dict: Dictionary containing path parameters extracted from the request.
    """
    resolved = resolve(request.path_info)
    request.path_params = resolved.kwargs
    return request.path_params

def get_request_fields(request: Any) -> ApiRequest:
    """
    Extract relevant fields from an HTTP request for API monitoring.
    Args:
        request (Any): The HTTP request object.
    Returns:
        ApiRequest: An object containing relevant fields extracted from the request.
    """
    mask_options = MaskOptions(mask_with='*', fields=['authorization'], prefixes=['x-'])

    def get_request_body(request: Any) -> Optional[Dict[str, Any]]:
        """
        Extract the request body from an HTTP request.
        Args:
            request (Any): The HTTP request object.
        Returns:
            Optional[Dict[str, Any]]: The parsed request body as a dictionary, or None if the request body
            is empty or cannot be parsed.
        """
        content_type = request.headers.get('Content-Type', '')
        if is_empty(request):
            return None
        else:
            if content_type.startswith('application/json'):
                try:
                    # Parse the byte string directly without decoding
                    json_data = json.loads(request.body)
                    return json_data
                except json.JSONDecodeError as e:
                    logging.error(f"Error decoding JSON: {e}")
                    return {}
            elif content_type.startswith('application/x-www-form-urlencoded'):
                return QueryDict(request.body.decode('utf-8'))
            elif content_type.startswith('multipart/form-data'):
                return parse_multipart_body(request)
            else:
                decoded_raw_body = request.body.decode('utf-8')
                if (decoded_raw_body == ""):
                    return {}
                return {'raw_body': decoded_raw_body}

    request_details = RequestDetails(
        headers=mask_data(dict(request.headers), mask_options),
        userAgent=request.headers.get('user-agent'),
        cookies=dict(request.COOKIES),
        ip=request.META.get('REMOTE_ADDR'),
        requestBody=get_request_body(request),
        protocol=request.scheme,
        hostName=request.META.get('HTTP_HOST'),
        query=dict(request.GET),
        subdomains=[] if request.META.get('HTTP_HOST', '').count('.') == 3 else request.META.get('HTTP_HOST', '').split('.')[:-2],
        uaVersionBrand=request.headers.get('sec-ch-ua'),
        uaMobile=request.headers.get('sec-ch-ua-mobile'),
        uaPlatform=request.headers.get('sec-ch-ua-platform'),
        reqAcceptEncoding=request.headers.get('accept-encoding'),
        reqAcceptLanguage=request.headers.get('accept-language'),
        rawHeaders=list(request.headers.items()),
        remoteAddress=request.META.get('REMOTE_ADDR'),
        remoteFamily=request.META.get('REMOTE_FAMILY', None),
        path=request.path or request.get_full_path(),
        params=extract_path_params(request)
    )

    return ApiRequest(
        host=request.headers.get('host'),
        httpMethod=request.method,
        url=request.build_absolute_uri(),
        originalUrl=request.build_absolute_uri(),
        baseUrl=request.build_absolute_uri('/')[:-1],
        httpVersion=int(round(float(request.META.get('SERVER_PROTOCOL', 'HTTP/1.0').split('/')[-1]))),
        request_details=request_details
    )

def get_response_fields(response: Any) -> ApiResponse:
    """
    Extract relevant fields from an HTTP response for API monitoring.
    Args:
        response (Any): The HTTP response object.
    Returns:
        ApiResponse: An object containing relevant fields extracted from the response.
    """
    return ApiResponse(
        responseStatusCode=response.status_code,
        responseStatusMessage=response.reason_phrase,
        responseBody=response.content.decode('utf-8'),
        responseHeaders=dict(response.items())
    )

def is_monitor_api(request: Any, method: HttpMethod, path: str, options: Optional[ExcludeOptions] = None) -> bool:
    """
    Check if an API endpoint should be monitored based on exclusion options.
    Args:
        request (Any): The HTTP request object.
        method (HttpMethod): The HTTP method of the request.
        path (str): The path of the API endpoint.
        options (Optional[ExcludeOptions]): Options for excluding certain API endpoints from monitoring
        (default None).

    Returns:
        bool: True if the API endpoint should be monitored, False otherwise.
    """
    monitor_api = True
    if options is None:
        return monitor_api
    elif method in options.__dict__ and options.__dict__[method]:
        for exclude_path in options.__dict__[method]:
            params = extract_path_params(request)
            if params:
                if path == generate_path(exclude_path, params):
                    monitor_api = False
                    break
            elif path == exclude_path:
                monitor_api = False
                break
    return monitor_api
