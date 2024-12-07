from nexios.http import response,request
from nexios.validator import Schema
from nexios.http.response import NexioResponse
import traceback
class APIHandler:
    allowed_methods = ['get','post','delete','put','patch','options']
    async def handle_error(self, error: Exception, request: request.Request, response: response.NexioResponse) -> response.NexioResponse:
        error  = traceback.format_exc()
        print(error)
    async def before_request(self, request: request.Request, response: response.NexioResponse):
        
        
        pass
    
    async def after_request(self, request: request.Request, response: response.NexioResponse):
        """Hook that runs after each request"""

    async def __call__(self, request: request.Request, response:response.NexioResponse) -> response.NexioResponse:
        method = request.method.lower()
        if method not in self.allowed_methods:
            return response.json("Method not allowed",status_code=405)
        
        handler = getattr(self, method, None)
        validator = getattr(self,f"validate_{method}",None)
        if  validator  and issubclass(validator,Schema):
            request._validation_schema = validator
            request._validation_errors = {}
            request._validated_data = None
        
        if not callable(handler):
            return response.status(405)
        try:
            before_request = await self.before_request(request, response)
            if isinstance(before_request,NexioResponse):
                return before_request
            
            _response = await handler(request,response)
            await self.after_request(request,response)

            return _response

            
        
        except Exception as e:
            
            await self.handle_error(e,request,response)
        