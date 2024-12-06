from django.conf import settings
from datetime import datetime, timezone
from foxsenseinnovations.vigil.vigil_utils.api_monitoring_utils_django import get_request_fields, get_response_fields, is_monitor_api, generate_path
from foxsenseinnovations.vigil.vigil import Vigil
from foxsenseinnovations.vigil.vigil_types.api_monitoring_types import ApiMonitoringOptions
from foxsenseinnovations.vigil.api_service import ApiService
from foxsenseinnovations.vigil.constants.route_constants import RouteConstants
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
class ApiMonitoringMiddleware:
    """
    ApiMonitoringMiddleware captures and monitors API requests and responses in a Django application.
    It utilizes the Vigil API monitoring system to record and analyze interactions, capturing details like
    headers, parameters, and timing. Integration provides insights for performance optimization and debugging.
    """
    def __init__(self, get_response):
        """
        Initializes the ApiMonitoringMiddleware with the given get_response function.
        Args:
            get_response: A function to get the response for the request.
        Returns:
            None
        """
        self.get_response = get_response
        self.options = getattr(settings, 'API_MONITORING_OPTIONS', ApiMonitoringOptions())

    def __call__(self, request):
        """
        Handles incoming API requests and outgoing responses. Captures API data and sends it to the Vigil
        API monitoring system.
        Args:
            request: The incoming HTTP request.
        Returns:
            The HTTP response.
        """
        start_time = datetime.now(timezone.utc).isoformat()
        request.original_body = request.body
        monitor_api = is_monitor_api(
            request,
            request.method,
            request.path if request.path else request.get_full_path(),
            getattr(self.options, 'exclude', None)
        )

        response = self.get_response(request)

        if monitor_api:
            end_time = datetime.now(timezone.utc).isoformat()
            api_request = get_request_fields(request)
            api_response = get_response_fields(response)
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
                "params": api_request.request_details["params"]
            }
            data = {
                'clientVersion': self.options.clientVersion if self.options.clientVersion is not None else Vigil.version,
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
                logging.info(f"[Vigil] API monitoring record created successfully for the API - {generate_path(request.path or request.get_full_path(), request.GET)}")
            except Exception as err:
                logging.error(f"[Vigil] Error while creating API monitoring record: {err}")

        return response
