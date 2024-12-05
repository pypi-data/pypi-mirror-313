
#TODO : deletation of sessions


from nexios.sessions.backends.db import SessionStore as DBSessionStore
from nexios.http.request import Request
from nexios.http.response import NexioResponse
from nexios.middlewares.base import BaseMiddleware
class SessionMiddleware(BaseMiddleware):
    async def process_request(self, request:Request, response):
        
        #TODO:ALLOW TO USE THE SETTING TO CHANGE SESSION KEY NAME

        key = request.cookies.get("session_id")
        session = DBSessionStore(session_key=key, 
                               config=request.scope['config'])
        self.session = session
        
        request.session = session
        



    async def process_response(self, request, response :NexioResponse):
        
        if self.session.modified:
            await self.session.save() 
            response.set_cookie(
                key="session_id",
                value=self.session.session_key
            )