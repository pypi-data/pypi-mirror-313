from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import ClosingIterator
from foxsenseinnovations.vigil.vigil_utils.api_monitoring_utils_flask import get_request_fields, get_response_fields, is_monitor_api, generate_path
from datetime import datetime, timezone
from foxsenseinnovations.vigil.vigil import Vigil
from foxsenseinnovations.vigil.vigil_types.api_monitoring_types import ApiMonitoringOptions
from foxsenseinnovations.vigil.api_service import ApiService
from foxsenseinnovations.vigil.constants.route_constants import RouteConstants
from io import BytesIO
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
class ApiMonitoringMiddleware:
    """
    ApiMonitoringMiddleware captures and monitors API requests and responses in a Flask application.
    It utilizes the Vigil API monitoring system to record and analyze interactions, capturing details like
    headers, parameters, and timing. Integration provides insights for performance optimization and debugging.
    """
    def __init__(self, app, options=None):
        if options is None:
            options = ApiMonitoringOptions()
        self.app = app.wsgi_app
        self.url_map = app.url_map 
        self.adapter = self.url_map.bind('')
        self.options = options

    def extract_path_params(self, path_info, method):
        """
        Extracts path parameters dynamically using Flask's URL map.
        Args:
            path_info: The request path.
            request: The Flask request object.
        Returns:
            path_params: A dictionary of path parameters.
        """
        path_params = {}
        try:
            # Iterate through the URL rules to find the matching rule
            endpoint, args = self.adapter.match(path_info, method=method)                   # Extract parameters from the matched rule
            path_params = args
        except Exception as e:
            path_params={}
        return path_params

    def __call__(self, environ, start_response):
        try:
            """
            Handles incoming API requests and outgoing responses. Captures API data and sends it to the Vigil
            API monitoring system.
            Args:
                request: The incoming HTTP request.
            Returns:
                The HTTP response.
            """
            start_time = datetime.now(timezone.utc).isoformat()
            request = Request(environ)
            monitor_api = is_monitor_api(
                        request.method,
                        request.path if request.path else request.full_path,
                        getattr(self.options, 'exclude', None)
                    )
            
            raw_data = request.get_data(cache=True, parse_form_data=False)
            environ['wsgi.input'] = BytesIO(raw_data)
            # Create a list to store status code and message
            status_code_message = []

            def custom_start_response(status, headers, exc_info=None):
                status_code_message.append(status)
                return start_response(status, headers, exc_info)

            # Wrap the original start_response with the custom_start_response
            app_iter = self.app(environ, custom_start_response)

            # Convert app_iter to a list
            app_iter_list = list(app_iter)

            # Use the status code and message captured by custom_start_response
            response = Response(app_iter_list, status=status_code_message[0])

            if monitor_api:
                end_time = datetime.now(timezone.utc).isoformat()
                api_request = get_request_fields(request)
                api_response = get_response_fields(response)
                path_params = path_params = self.extract_path_params(request.path, request.method)
                request_data = {
                    "host": api_request.host,
                    "userAgent": api_request.request_details["userAgent"],
                    "httpMethod": api_request.httpMethod,
                    "cookies": api_request.request_details["cookies"],
                    "ip": api_request.request_details["ip"],
                    "headers": api_request.request_details["headers"],
                    "requestBody": api_request.request_details["requestBody"],
                    "protocol": api_request.request_details["protocol"],
                    "hostName": api_request.request_details["hostName"],
                    "url": api_request.url,
                    "path": api_request.request_details["path"],
                    "originalUrl": api_request.originalUrl,
                    "baseUrl": api_request.baseUrl,
                    "query": api_request.request_details["query"],
                    "subDomains": api_request.request_details["subdomains"],
                    "uaVersionBrand": api_request.request_details["uaVersionBrand"],
                    "uaMobile": api_request.request_details["uaMobile"],
                    "uaPlatform": api_request.request_details["uaPlatform"],
                    "reqAcceptEncoding": api_request.request_details["reqAcceptEncoding"],
                    "reqAcceptLanguage": api_request.request_details["reqAcceptLanguage"],
                    "rawHeaders": api_request.request_details["rawHeaders"],
                    "httpVersion": api_request.httpVersion,
                    "remoteAddress": api_request.request_details["remoteAddress"],
                    "remoteFamily": api_request.request_details["remoteFamily"],
                    "params": path_params
                }
                data = {
                    'clientVersion': self.options.clientVersion if self.options.clientVersion != None else Vigil.version,
                    'startTime': start_time,
                    'endTime': end_time,
                    'request': request_data,
                    'response': api_response.__dict__
                }
                try:
                    ApiService.make_api_call(
                        Vigil.instance_url,
                        RouteConstants.API_MONITORING,
                        data,
                        Vigil.api_key
                    )
                    logging.info(f"[Vigil] API monitoring record created successfully for the API - {generate_path(request.path or request.url, request.args)}")
                except Exception as err:
                    logging.error(f"[Vigil] Error while creating API monitoring record: {err}")
            app_iter_rewind = iter(app_iter_list)
            return ClosingIterator(app_iter_rewind, response.close)
        except Exception as e:
                logging.error(f"[Vigil] Error while creating API monitoring record: {e}")
