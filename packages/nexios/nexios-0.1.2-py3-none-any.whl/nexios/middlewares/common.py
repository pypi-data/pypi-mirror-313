from nexios.middlewares.base import BaseMiddleware
from nexios.http.response import NexioResponse
from nexios.http.request import Request

class CommonMiddleware(BaseMiddleware):
    async def process_request(self, request: Request, response):
        
        pass

    async def process_response(self, request: Request, response: NexioResponse):
        response.headers['Content-Type'] = 'application/json'  
        response.headers['X-Frame-Options'] = 'DENY'  
        response.headers['X-XSS-Protection'] = '1; mode=block'  
        response.headers['X-Content-Type-Options'] = 'nosniff'  
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'  
        response.headers['Cache-Control'] = 'no-store'  
        
        if request.user_agent:
            response.headers['X-User-Agent'] = request.user_agent 


        return response
