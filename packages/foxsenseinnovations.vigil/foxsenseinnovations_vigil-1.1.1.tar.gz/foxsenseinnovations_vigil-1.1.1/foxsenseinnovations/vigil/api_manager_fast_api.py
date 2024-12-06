from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from foxsenseinnovations.vigil.vigil_utils.api_monitoring_utils_fast_api import (
    get_request_fields, get_response_fields, is_monitor_api, generate_path
)
from foxsenseinnovations.vigil.vigil import Vigil
from foxsenseinnovations.vigil.vigil_types.api_monitoring_types import ApiMonitoringOptions
from foxsenseinnovations.vigil.api_service import ApiService
from foxsenseinnovations.vigil.constants.route_constants import RouteConstants
from datetime import datetime, timezone
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

class ApiMonitoringMiddleware(BaseHTTPMiddleware):
    """
    Middleware for monitoring API requests and responses in FastAPI.
    Captures request/response data and sends it to the Vigil monitoring system.
    """

    def __init__(self, app: FastAPI, options: ApiMonitoringOptions = None):
        super().__init__(app)
        self.options = options if options else ApiMonitoringOptions()

    async def dispatch(self, request: Request, call_next):
        try:
            # Start time for the request
            start_time = datetime.now(timezone.utc).isoformat()

            body_bytes = await request.body() 
            request_body = body_bytes.decode() 
            request.state.request_body = request_body
            request._body = body_bytes
            # Check if the API should be monitored
            monitor_api = is_monitor_api(
                request.method,
                str(request.url.path),
                getattr(self.options, "exclude", None),
            )

            
            # Capture the response
            response = None
            response_body = b""
            try:
                original_response = await call_next(request)
                response_body = b"".join([chunk async for chunk in original_response.body_iterator])
                response = Response(
                    content=response_body,
                    status_code=original_response.status_code,
                    headers=original_response.headers,
                    media_type=original_response.media_type
                )   
            except Exception as e:
                logging.error(f"[Vigil] Error while processing request: {e}")
                raise

            # End time for the request
            end_time = datetime.now(timezone.utc).isoformat()

            if monitor_api:
                # Extract request and response fields
                api_request = await get_request_fields(request)
                api_response = get_response_fields(response)
                
                # Build the request data
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
                    "params": api_request.request_details["params"],  
                }

                # Prepare data for Vigil
                data = {
                    "clientVersion": self.options.clientVersion
                    if self.options.clientVersion
                    else Vigil.version,
                    "startTime": start_time,
                    "endTime": end_time,
                    "request": request_data,
                    "response": api_response.__dict__,
                }

                try:
                    ApiService.make_api_call(
                        Vigil.instance_url,
                        RouteConstants.API_MONITORING,
                        data,
                        Vigil.api_key,
                    )
                    logging.info(
                        f"[Vigil] API monitoring record created successfully for the API - {generate_path(request.url.path, request.query_params)}"
                    )
                except Exception as err:
                    logging.error(
                        f"[Vigil] Error while creating API monitoring record: {err}"
                    )
            
            return response
        except Exception as e:
            logging.error(f"[Vigil] Error while creating API monitoring record: {e}")
