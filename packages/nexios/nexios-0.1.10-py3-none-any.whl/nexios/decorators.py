from enum import Enum
from typing import List,Union
from .http.request import Request
from .http.response import NexioResponse
from .http.request import Request
import typing
from functools import wraps
from .types import HTTPMethod


class RouteDecorator:
    """Base class for all route decorators"""
    def __init__(self):
        self.handler = None

    async def __call__(self, request: Request, response: NexioResponse, **kwargs):
        if self.handler:
            return await self.handler(request, response, **kwargs)
        raise NotImplementedError("Handler not set")

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.__class__(obj)
    


class AllowedMethods(RouteDecorator):
    def __init__(self, methods: List[Union[str, HTTPMethod]]):
        super().__init__()
        self.allowed_methods = [method.upper() if isinstance(method, str) else method.value 
                              for method in methods]

    def __call__(self, handler):
        @wraps(handler)
        async def wrapper(request: Request, response: NexioResponse, **kwargs):
            if request.method.upper() not in self.allowed_methods:
                return response.json({
                    "error": f"Method {request.method} not allowed",
                    "allowed_methods": self.allowed_methods
                },status_code=405)
            return await handler(request, response, **kwargs)
        return wrapper 
    

def validate_request(
        schema :typing.Dict[str,typing.List[typing.Callable]]
        ):

    def decorator(handler):

        @wraps(handler)
        async def wrapper(request :Request, response    :NexioResponse):
            request._validation_schema = schema
            request._validation_errors = {}
            request._validated_data = None

            return await handler(request,response)
        
        return wrapper 

    return decorator