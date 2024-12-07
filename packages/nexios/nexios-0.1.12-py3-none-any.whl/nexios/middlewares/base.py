from nexios.http.response import NexioResponse
class BaseMiddleware:
    def __init__(self,*kwargs) -> None:
        pass
    async def __call__(self, request, response, next_middleware):
        """Call the middleware process and pass control to the next middleware in the stack."""
        await self.process_request(request, response)
        await next_middleware()
        await self.process_response(request, response)
        


    async def process_request(self, request, response):
        """Override this method in child classes to process the request before passing it along."""
        pass

    async def process_response(self, request, response):
        """Override this method in child classes to process the response before returning it."""
        pass
