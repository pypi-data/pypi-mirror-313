from typing import Any, Dict, Optional, List
from foxsenseinnovations.vigil.vigil_types.api_monitoring_types import ApiRequest, ApiResponse, ExcludeOptions, RequestDetails
from foxsenseinnovations.vigil.enums.http_method_enum import HttpMethod
from foxsenseinnovations.vigil.vigil_utils.common_utils import MaskOptions, mask_data, generate_path
import json
import re
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
        'filename': file.filename,
        'content': file_content,
    }


def parse_multipart_body(request):
    try:
        """
        Parse multipart request body and extract data.
        Args:
            request: The HTTP request object.
        Returns:
            Dict[str, Any]: Parsed data from the request body.
        """
        data = dict(request.form)
        files_data = {key: serialize_file(file) for key, file in request.files.items()}
        data.update(files_data)
        return data
    except Exception as e:
            logging.error(f"[Vigil] Error while parsing multipart body: {e}")
            raise


def _is_empty_request(request: Any) -> bool:
    try:
        """
        Check if an HTTP request is empty.
        Args:
            request: The HTTP request object.
        Returns:
            bool: True if the request is empty, False otherwise.
        """
        return request.data == b'' and not bool(request.form) and len(request.form)==0 and len(request.files)==0
    except Exception as e:
        logging.error(f"[Vigil] Error while checking the request body is empty: {e}")
        raise

def get_request_fields(request: Any) -> ApiRequest:
    try:
        """
        Extract relevant fields from an HTTP request for API monitoring.
        Args:
            request (Any): The HTTP request object.
        Returns:
            ApiRequest: An object containing relevant fields extracted from the request.
        """
        mask_options = MaskOptions(mask_with='*', fields=['authorization'], prefixes=['x-'])
        def get_request_body(request: Any) -> Optional[Dict[str, Any]]:
            try:
                """
                Extract the request body from an HTTP request.
                Args:
                    request (Any): The HTTP request object.
                Returns:
                    Optional[Dict[str, Any]]: The parsed request body as a dictionary, or None if the request body
                    is empty or cannot be parsed.
                """
                content_type = request.headers.get('Content-Type', '')
                if _is_empty_request(request):
                    return None
                else:
                    if content_type.startswith('application/json'):
                        try:
                            # Parse the byte string directly without decoding
                            json_data = json.loads(request.data)
                            return json_data
                        except json.JSONDecodeError as e:
                            logging.error(f"Error decoding JSON: {e}")
                            return {}
                    elif content_type.startswith('application/x-www-form-urlencoded'):
                        return dict(request.form)
                    elif content_type.startswith('multipart/form-data'):
                        return parse_multipart_body(request)
                    else:
                        decoded_raw_body = request.data.decode('utf-8')
                        if (decoded_raw_body == ""):
                            return {}
                        return {'raw_body': decoded_raw_body}
            except Exception as e:
                logging.error(f"[Vigil] Error while extracting the request body: {e}")
                raise

        request_details = RequestDetails(
            headers=mask_data(dict(request.headers), mask_options),
            userAgent=request.headers.get('user-agent'),
            cookies=dict(request.cookies),
            ip=request.remote_addr,
            requestBody=get_request_body(request),
            protocol=request.scheme,
            hostName=request.host,
            query=request.args.to_dict(flat=False),
            subdomains=[] if request.environ.get('HTTP_HOST', '').count('.') == 3 else request.environ.get('HTTP_HOST', '').split('.')[:-2],
            uaVersionBrand=request.headers.get('sec-ch-ua'),
            uaMobile=request.headers.get('sec-ch-ua-mobile'),
            uaPlatform=request.headers.get('sec-ch-ua-platform'),
            reqAcceptEncoding=request.headers.get('accept-encoding'),
            reqAcceptLanguage=request.headers.get('accept-language'),
            rawHeaders=list(request.headers.items()),
            remoteAddress=request.remote_addr,
            remoteFamily=request.environ.get('REMOTE_FAMILY', None),
            path=request.path or request.url,
            params=request.args.to_dict(flat=False)
        )

        return ApiRequest(
            host=request.headers.get('host'),
            httpMethod=request.method,
            url=request.url,
            originalUrl=request.url,
            baseUrl=request.host_url,
            httpVersion=int(round(float(request.environ.get('SERVER_PROTOCOL', 'HTTP/1.0').split('/')[-1]))),
            request_details=request_details
        )
    except Exception as e:
            logging.error(f"[Vigil] Error while extracting request fields: {e}")
            raise

def get_response_fields(response: Any) -> ApiResponse:
    try:
        """
        Extract relevant fields from an HTTP response for API monitoring.
        Args:
            response (Any): The HTTP response object.
        Returns:
            ApiResponse: An object containing relevant fields extracted from the response.
        """
        return ApiResponse(
            responseStatusCode=response.status_code,
            responseStatusMessage=" ".join(response.status.split()[1:]),
            responseBody=response.get_data(as_text=True),
            responseHeaders=dict(response.headers)
        )
    except Exception as e:
            logging.error(f"[Vigil] Error while extracting response fields: {e}")
            raise

def extract_path_params(route_pattern, path):
    try:
        """
        Extract path parameters from a URL path based on a route pattern.
        Args:
            route_pattern (str): The route pattern containing placeholders for parameters.
            path (str): The URL path to extract parameters from.
        Returns:
            dict: Dictionary containing extracted path parameters.
        """
        # Escape special characters in the route pattern
        pattern = re.escape(route_pattern)

        # Replace route parameters with a capturing group
        pattern = re.sub(r'<(\w+)>', r'(?P<\1>[^/]+)', pattern)

        # Replace type-specific parameters (e.g., <int:parameter>)
        pattern = re.sub(r'<(\w+):([^>]+)>', lambda m: f'(?P<{m.group(2)}>[^/]+)', pattern)

        # Match the path against the pattern
        match = re.match(pattern, path)

        if match:
            # Extract named groups as path parameters
            path_params = match.groupdict()
            return path_params
        else:
            return {}
    except Exception as e:
        logging.error(f"[Vigil] Error while extracting path params: {e}")
        raise
    

def is_monitor_api(method: HttpMethod, path: str, options: Optional[ExcludeOptions] = None) -> bool:
    try:
        """
        Check if an API endpoint should be monitored based on exclusion options.
        Args:
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
                params = extract_path_params(exclude_path, path)
                if params:
                    if path == generate_path(exclude_path, params):
                        monitor_api = False
                        break
                elif path == exclude_path:
                    monitor_api = False
                    break
        return monitor_api
    except Exception as e:
            logging.error(f"[Vigil] Error while checking to monitor API: {e}")
            raise