import traceback
import logging
import typing
from nexios.http.request import Request
from nexios.http.response import NexioResponse
from .base import BaseMiddleware
# Setting up a logger for middleware
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
# You can also configure more advanced logging handlers (e.g., logging to a file, database, or external service).

class ErrorHandlerMiddleware(BaseMiddleware):
    """
    A middleware class for handling errors globally within the application.
    This class processes requests and responses, capturing errors and logging them.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Any additional initialization can be done here
        self.error_status_code = 500
        self.error_message = "An unexpected error occurred"

    async def process_request(self, request: Request, response: NexioResponse) -> None:
        """
        Process the request before passing it along to the next middleware.
        We can add logging or any preprocessing before the request reaches the main handler.
        """
        pass

    async def process_response(self, request: Request, response: NexioResponse) -> None:
        """
        Process the response after the request has been handled by the main application or other middleware.
        This is where we can log success responses or handle any post-processing.
        """
        pass

    async def __call__(self, request: Request, response: NexioResponse, next_middleware: typing.Callable) -> NexioResponse:
        """
        The core method of the middleware, which processes the request, handles the error, and processes the response.
        """
        try:
            # Let the next middleware or route handler process the request
            response = await next_middleware()
        except Exception as error:
            # Capture and log the exception details
            self._log_error(traceback.format_exc())

            # Modify the response object to reflect an error
            return  response.send("Server error",status_code=500)
            

        return response

    def _log_error(self, error: Exception) -> None:
        """
        A helper method to log the error details in a structured and configurable way.
        This can be expanded to log to files, external monitoring services, etc.
        """
        # Log the error with traceback for full context
        logger.error(f"Unhandled exception: {str(error)}")
        logger.debug("Error traceback: %s", traceback.format_exc())
