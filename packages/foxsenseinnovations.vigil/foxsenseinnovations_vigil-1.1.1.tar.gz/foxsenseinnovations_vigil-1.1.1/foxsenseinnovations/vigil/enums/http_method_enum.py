from enum import Enum

class HttpMethod(Enum):
    """
    Enum representing HTTP methods.
    Attributes:
        GET: Represents the HTTP GET method.
        POST: Represents the HTTP POST method.
        PUT: Represents the HTTP PUT method.
        PATCH: Represents the HTTP PATCH method.
        DELETE: Represents the HTTP DELETE method.
    """
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
