import re
from nexios.middlewares.base import BaseMiddleware
from nexios.http.response import NexioResponse
from nexios.http.request import Request
from typing import Sequence

ALL_METHODS = ("DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT")
BASIC_HEADERS = {"Accept", "Accept-Language", "Content-Language", "Content-Type"}
SAFELISTED_HEADERS = {"Accept", "Accept-Language", "Content-Language", "Content-Type"}

class CORSMiddleware(BaseMiddleware):
    def __init__(
        self,
        allow_origins: Sequence[str] = (),
        blacklist_origins: Sequence[str] = (),
        allow_methods: Sequence[str] = ALL_METHODS,
        allow_headers: Sequence[str] = (),
        blacklist_headers: Sequence[str] = (),
        allow_credentials: bool = False,
        allow_origin_regex: str | None = None,
        expose_headers: Sequence[str] = (),
        max_age: int = 600,
    ):
        super().__init__()
        
        if allow_methods is None:
            allow_methods = ALL_METHODS
        if allow_origins is None:
            allow_origins = []
        if blacklist_origins is None:
            blacklist_origins = []
        if allow_headers is None:
            allow_headers = list(BASIC_HEADERS)
        if blacklist_headers is None:
            blacklist_headers = []
        if allow_credentials is None:
            allow_credentials = False
        if expose_headers is None:
            expose_headers = []
        if max_age is None:
            max_age = 600

        # Ensure that allow_methods includes all methods if "*" is specified
        if "*" in allow_methods:
            allow_methods = ALL_METHODS

        self.allow_origins = allow_origins
        self.blacklist_origins = blacklist_origins
        self.allow_methods = allow_methods

        # Allow all basic headers by default unless specific headers are provided
        self.allow_headers = [h.lower() for h in allow_headers] or list(BASIC_HEADERS)
        
        # Add the blacklisted headers to the list of allowed headers
        self.blacklist_headers = [h.lower() for h in blacklist_headers]

        self.allow_credentials = allow_credentials
        self.allow_origin_regex = re.compile(allow_origin_regex) if allow_origin_regex else None
        self.expose_headers = expose_headers
        self.max_age = max_age

        # Prepare the simple headers to include the Allow-Origin and Allow-Credentials headers if applicable
        self.simple_headers = {}
        if "*" in allow_origins:
            self.simple_headers["Access-Control-Allow-Origin"] = "*"
        if allow_credentials:
            self.simple_headers["Access-Control-Allow-Credentials"] = "true"
        if expose_headers:
            self.simple_headers["Access-Control-Expose-Headers"] = ", ".join(expose_headers)

        # Prepare preflight headers with methods and max age
        self.preflight_headers = {
            "Access-Control-Allow-Methods": ", ".join(allow_methods),
            "Access-Control-Max-Age": str(max_age),
        }
        if allow_credentials:
            self.preflight_headers["Access-Control-Allow-Credentials"] = "true"

    async def process_request(self, request: Request, response):
        
        method = request.scope["method"]
        origin = request.headers.get("origin")

        if method == "OPTIONS" and "access-control-request-method" in request.headers:
            return await self.preflight_response(request, response)

        if origin:
            request.scope['cors_origin'] = origin

    async def process_response(self, request: Request, response: NexioResponse):
        origin = request.scope.get('cors_origin')

        if origin and self.is_allowed_origin(origin):
            response.headers["Access-Control-Allow-Origin"] = origin

            if self.allow_credentials:
                response.headers["Access-Control-Allow-Credentials"] = "true"

        if self.expose_headers:
            response.headers["Access-Control-Expose-Headers"] = ", ".join(self.expose_headers)

        return response

    def is_allowed_origin(self, origin: str) -> bool:
        if origin in self.blacklist_origins:
            return False

        if "*" in self.allow_origins:
            return True

        if self.allow_origin_regex and self.allow_origin_regex.fullmatch(origin):
            return True

        return origin in self.allow_origins

    async def preflight_response(self, request: Request, response: NexioResponse) -> NexioResponse:
        origin = request.headers.get("origin")
        requested_method = request.headers.get("access-control-request-method")
        requested_headers = request.headers.get("access-control-request-headers")

        headers = self.preflight_headers.copy()

        if self.is_allowed_origin(origin):
            headers["Access-Control-Allow-Origin"] = origin
        else:
            return NexioResponse("Disallowed CORS Origin", status_code=400, headers=headers)

        if requested_method not in self.allow_methods:
            return response.json("Disallowed CORS Method", status_code=400, headers=headers)

        if requested_headers:
            allowed_headers = [h.strip().lower() for h in requested_headers.split(",")]
            if not all(h in self.allow_headers or h in SAFELISTED_HEADERS for h in allowed_headers):
                if any(h in self.blacklist_headers for h in allowed_headers):
                    return response.json("Disallowed CORS Headers", status_code=400, headers=headers)

        return response.json("OK", status_code=200, headers=headers)
