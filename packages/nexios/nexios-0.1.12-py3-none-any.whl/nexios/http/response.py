from datetime import datetime, timedelta
from email.utils import formatdate
from typing import Any, Dict, List, Optional, Tuple, Union, BinaryIO
from pathlib import Path
import json
from base64 import b64encode
from hashlib import sha1
import mimetypes
import os
from time import time
import typing


class Response:
    """
    Base ASGI-compatible Response class with support for cookies, caching, and custom headers.
    """
    
    STATUS_CODES = {
        200: "OK",
        201: "Created",
        204: "No Content",
        301: "Moved Permanently",
        302: "Found",
        304: "Not Modified",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        500: "Internal Server Error",
    }

    def __init__(
        self,
        body: Union[str, bytes, dict] = "",
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        content_type: str = "text/plain",
    ):
        self.status_code = status_code
        self._headers = {}
        self._cookies: List[Tuple[str, str, dict]] = []
        
        # Initialize headers
        self.headers = headers or {}
        
        # Set body and content type
        if isinstance(body, dict):
            self._body = json.dumps(body).encode('utf-8')
            self.content_type = "application/json"
        elif isinstance(body, str):
            self._body = body.encode('utf-8')
            self.content_type = content_type
        elif isinstance(body, bytes):
            self._body = body
            self.content_type = content_type
        else:
            raise TypeError("Body must be str, bytes, or dict")

        # Set content length
        self.headers['content-length'] = str(len(self._body))
        self.headers['content-type'] = self.content_type

    @property
    def headers(self) -> Dict[str, str]:
        """Get all headers including cookies."""
        headers = self._headers.copy()
        if self._cookies:
            # Return multiple Set-Cookie headers as a list
            headers['set-cookie'] = [
                self._serialize_cookie(key, value, options)
                for key, value, options in self._cookies
            ]
        return headers

    @headers.setter
    def headers(self, headers: Dict[str, str]) -> None:
        """Set headers with case-insensitive keys."""
        self._headers = {k.lower(): v for k, v in headers.items()}

    def set_cookie(
        self,
        key: str,
        value: str,
        max_age: Optional[int] = None,
        expires: Optional[Union[str, datetime]] = None,
        path: str = "/",
        domain: Optional[str] = None,
        secure: bool = False,
        httponly: bool = False,
        samesite: Optional[str] = None
    ) -> None:
        """Set a cookie with the given parameters."""
        cookie_options = {}
        
        if max_age is not None:
            cookie_options['max-age'] = str(max_age)
        
        if expires is not None:
            if isinstance(expires, datetime):
                cookie_options['expires'] = formatdate(expires.timestamp(), usegmt=True)
            else:
                cookie_options['expires'] = expires
        
        if path is not None:
            cookie_options['path'] = path
            
        if domain is not None:
            cookie_options['domain'] = domain
            
        if secure:
            cookie_options['secure'] = True
            
        if httponly:
            cookie_options['httponly'] = True
            
        if samesite is not None:
            cookie_options['samesite'] = samesite
            
        self._cookies.append((key, value, cookie_options))

    def delete_cookie(self, key: str, path: str = "/", domain: Optional[str] = None) -> None:
        """Delete a cookie by setting its expiry to the past."""
        self.set_cookie(
            key=key,
            value="",
            max_age=0,
            expires="Thu, 01 Jan 1970 00:00:00 GMT",
            path=path,
            domain=domain
        )

    def enable_caching(self, max_age: int = 3600, private: bool = True) -> None:
        """Enable caching with the specified max age (in seconds)."""
        cache_control = []
        if private:
            cache_control.append("private")
        else:
            cache_control.append("public")
            
        cache_control.append(f"max-age={max_age}")
        self.headers["cache-control"] = ", ".join(cache_control)
        
        etag = self._generate_etag()
        self.headers["etag"] = etag
        
        expires = datetime.utcnow() + timedelta(seconds=max_age)
        self.headers["expires"] = formatdate(expires.timestamp(), usegmt=True)

    def disable_caching(self) -> None:
        """Disable caching for this response."""
        self.headers["cache-control"] = "no-store, no-cache, must-revalidate, max-age=0"
        self.headers["pragma"] = "no-cache"
        self.headers["expires"] = "0"

    async def __call__(self, scope: dict, receive: typing.Callable, send: typing.Callable) -> None:
        """Make the response callable as an ASGI application."""
        headers = []
        for k, v in self.headers.items():
            if k == 'set-cookie':
                # Handle multiple Set-Cookie headers
                if isinstance(v, list):
                    for cookie in v:
                        headers.append([b'set-cookie', cookie.encode('utf-8')])
                else:
                    headers.append([b'set-cookie', v.encode('utf-8')])
            else:
                headers.append([k.encode('utf-8'), v.encode('utf-8')])
        
        await send({
            'type': 'http.response.start',
            'status': self.status_code,
            'headers': headers,
        })
        
        await send({
            'type': 'http.response.body',
            'body': self._body,
        })

    def _serialize_cookie(self, key: str, value: str, options: dict) -> str:
        """Serialize a single cookie into a Set-Cookie header value."""
        cookie = f"{key}={value}"
        for opt_key, opt_value in options.items():
            if isinstance(opt_value, bool):
                if opt_value:
                    cookie += f"; {opt_key}"
            else:
                cookie += f"; {opt_key}={opt_value}"
        return cookie

    def _generate_etag(self) -> str:
        """Generate an ETag for the response content."""
        content_hash = sha1()
        content_hash.update(self._body)
        return f'W/"{b64encode(content_hash.digest()).decode("utf-8")}"'


class JSONResponse(Response):
    """
    Response subclass for JSON content.
    """
    def __init__(
        self,
        content: Any,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        indent: Optional[int] = None,
        ensure_ascii: bool = True,
    ):
        try:
            body = json.dumps(
                content,
                indent=indent,
                ensure_ascii=ensure_ascii,
                allow_nan=False,
                default=str
            )
        except (TypeError, ValueError) as e:
            raise ValueError(f"Content is not JSON serializable: {str(e)}")
            
        super().__init__(
            body=body,
            status_code=status_code,
            headers=headers,
            content_type="application/json"
        )


class HTMLResponse(Response):
    """
    Response subclass for HTML content.
    """
    def __init__(
        self,
        content: Union[str, bytes],
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(
            body=content,
            status_code=status_code,
            headers=headers,
            content_type="text/html; charset=utf-8"
        )


class FileResponse(Response):
    """
    Response subclass for file content with streaming support.
    """
    chunk_size = 64 * 1024  # 64KB chunks

    def __init__(
        self,
        path: Union[str, Path],
        filename: Optional[str] = None,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        content_disposition_type: str = "attachment",
    ):
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        if not self.path.is_file():
            raise ValueError(f"Path is not a file: {path}")
            
        self.filename = filename or self.path.name
        self.content_disposition_type = content_disposition_type
        self.status_code = status_code
        self._headers = {}
        self._cookies: List[Tuple[str, str, dict]] = []
        
        # Set headers
        self.headers = headers or {}
        
        # Determine content type
        content_type, _ = mimetypes.guess_type(str(self.path))
        self.content_type = content_type or 'application/octet-stream'
        self.headers['content-type'] = self.content_type
        
        # Set content disposition
        self.headers['content-disposition'] = f'{content_disposition_type}; filename="{self.filename}"'
        
        # Set content length
        self.headers['content-length'] = str(self.path.stat().st_size)

    async def __call__(self, scope: dict, receive: typing.Callable, send: typing.Callable) -> None:
        """Stream the file in chunks."""
        headers = []
        for k, v in self.headers.items():
            if k == 'set-cookie':
                if isinstance(v, list):
                    for cookie in v:
                        headers.append([b'set-cookie', cookie.encode('utf-8')])
                else:
                    headers.append([b'set-cookie', v.encode('utf-8')])
            else:
                headers.append([k.encode('utf-8'), v.encode('utf-8')])

        await send({
            'type': 'http.response.start',
            'status': self.status_code,
            'headers': headers,
        })

        with open(self.path, 'rb') as file:
            more_body = True
            while more_body:
                chunk = file.read(self.chunk_size)
                more_body = len(chunk) == self.chunk_size
                await send({
                    'type': 'http.response.body',
                    'body': chunk,
                    'more_body': more_body
                })


class StreamingResponse(Response):
    """
    Response subclass for streaming content.
    """
    def __init__(
        self,
        content: typing.Iterator[Union[str, bytes]],
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        content_type: str = "text/plain",
    ):
        self.content_iterator = content
        self.status_code = status_code
        self._headers = {}
        self._cookies: List[Tuple[str, str, dict]] = []
        
        # Set headers
        self.headers = headers or {}
        self.content_type = content_type
        self.headers['content-type'] = self.content_type
        
        # Streaming responses shouldn't have a content-length header
        self.headers.pop('content-length', None)

    async def __call__(self, scope: dict, receive: typing.Callable, send: typing.Callable) -> None:
        """Stream the content."""
        headers = []
        for k, v in self.headers.items():
            if k == 'set-cookie':
                if isinstance(v, list):
                    for cookie in v:
                        headers.append([b'set-cookie', cookie.encode('utf-8')])
                else:
                    headers.append([b'set-cookie', v.encode('utf-8')])
            else:
                headers.append([k.encode('utf-8'), v.encode('utf-8')])

        await send({
            'type': 'http.response.start',
            'status': self.status_code,
            'headers': headers,
        })

        for chunk in self.content_iterator:
            if isinstance(chunk, str):
                chunk = chunk.encode('utf-8')
            await send({
                'type': 'http.response.body',
                'body': chunk,
                'more_body': True
            })
            
        await send({
            'type': 'http.response.body',
            'body': b'',
            'more_body': False
        })


class RedirectResponse(Response):
    """
    Response subclass for HTTP redirects.
    """
    def __init__(
        self,
        url: str,
        status_code: int = 302,
        headers: Optional[Dict[str, str]] = None,
    ):
        if not 300 <= status_code < 400:
            raise ValueError("Status code must be a valid redirect status")
            
        headers = headers or {}
        headers['location'] = str(url)
        
        super().__init__(
            body="",
            status_code=status_code,
            headers=headers
        )


class NexioResponse:
    """
    A wrapper class that provides a fluent interface for different response types.
    """
    def __init__(self):
        self._status_code = 200
        self._body = None
        self._content_type = "application/json"
        self.headers = {}
        self._response = None
        self._cookies = []
        self._delete_cookies = []

    def send(self, content, status_code=200):
        """Send plain text or HTML content."""
        self._status_code = status_code
        self._body = content
        self._content_type = "text/plain"
        return self

    def json(self, data, status_code=None):
        """Send JSON response."""
        self._status_code = status_code or self._status_code or 200
        self._body = data
        self._content_type = "application/json"
        return self

    def html(self, content, status_code=200):
        """Send HTML response."""
        self._status_code = status_code
        self._body = content
        self._content_type = "text/html; charset=utf-8"
        return self

    def file(self, path, filename=None, content_disposition_type="attachment"):
        """Send file response."""
        self._response = FileResponse(
            path=path,
            filename=filename,
            status_code=self._status_code,
            headers=self.headers,
            content_disposition_type=content_disposition_type
        )
        return self

    def stream(self, iterator, content_type="text/plain"):
        """Send streaming response."""
        self._response = StreamingResponse(
            content=iterator,
            status_code=self._status_code,
            headers=self.headers,
            content_type=content_type
        )
        return self

    def redirect(self, url, status_code=302):
        """Send redirect response."""
        self._response = RedirectResponse(
            url=url,
            status_code=status_code,
            headers=self.headers
        )
        return self

    def status(self, status_code):
        """Set response status code."""
        self._status_code = status_code
        return self

    def header(self, key: str, value: str):
        """Set a response header."""
        self.headers[key.lower()] = str(value)
        return self

    def set_cookie(
        self,
        key: str,
        value: str,
        max_age: Optional[int] = None,
        expires: Optional[Union[str, datetime]] = None,
        path: str = "/",
        domain: Optional[str] = None,
        secure: bool = False,
        httponly: bool = False,
        samesite: Optional[str] = None
    ):
        """Set a response cookie."""
        self._cookies.append({
            'key': key,
            'value': value,
            'max_age': max_age,
            'expires': expires,
            'path': path,
            'domain': domain,
            'secure': secure,
            'httponly': httponly,
            'samesite': samesite
        })
        return self
    
    def delete_cookie(
        self,
        key: str,
        value: str = None,
        max_age: Optional[int] = None,
        expires: Optional[Union[str, datetime]] = None,
        path: str = "/",
        domain: Optional[str] = None,
        secure: bool = False,
        httponly: bool = False,
        samesite: Optional[str] = None
    ):
        """Set a response cookie."""
        self._delete_cookies.append({
            'key': key,
            'value': value,
            'max_age': max_age,
            'expires': expires,
            'path': path,
            'domain': domain,
            'secure': secure,
            'httponly': httponly,
            'samesite': samesite
        })
        return self

    def cache(self, max_age: int = 3600, private: bool = True):
        """Enable response caching."""
        if self._response is None:
            self._get_base_response().enable_caching(max_age, private)
        else:
            self._response.enable_caching(max_age, private)
        return self

    def no_cache(self):
        """Disable response caching."""
        if self._response is None:
            self._get_base_response().disable_caching()
        else:
            self._response.disable_caching()
        return self

    def _get_base_response(self):
        """Get the appropriate response type based on content type."""
        if self._response is not None:
            return self._response

        if self._content_type == "application/json":
            self._response = JSONResponse(
                content=self._body,
                status_code=self._status_code,
                headers=self.headers
            )
        elif self._content_type == "text/html; charset=utf-8":
            self._response = HTMLResponse(
                content=self._body,
                status_code=self._status_code,
                headers=self.headers
            )
        else:
            self._response = Response(
                body=self._body,
                status_code=self._status_code,
                headers=self.headers,
                content_type=self._content_type
            )

        # Apply cookies if any
        for cookie in self._cookies:
            self._response.set_cookie(**cookie)

        if len(self._delete_cookies) > 0:
            for cookie in self._delete_cookies:
                self._response.delete_cookie(cookie)

        return self._response

    async def __call__(self, scope, receive, send):
        """Make the response ASGI-compatible."""
        response = self._get_base_response()
        await response(scope, receive, send)