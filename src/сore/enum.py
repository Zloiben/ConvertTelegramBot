from enum import Enum

__all__ = (
    'HTTPMethods',
)


class HTTPMethods(Enum):
    GET = 'GET'
    POST = 'POST'
    DELETE = 'DELETE'
    PUT = 'PUT'
    PATCH = 'PATCH'
