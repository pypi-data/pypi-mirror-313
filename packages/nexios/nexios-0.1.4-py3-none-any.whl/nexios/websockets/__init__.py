from .base import WebSocket
async def get_websocket_session(scope,receive, send):
    ws = WebSocket(scope,receive,send)
    return ws 

