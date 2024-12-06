from functools import wraps
import asyncio
def run_sync(async_func):
    """Decorator to run async functions synchronously"""
    @wraps(async_func)
    def sync_wrapper(*args, **kwargs):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            # If no event loop exists, create a new one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        try:
            return loop.run_until_complete(async_func(*args, **kwargs))
        except Exception as e:
            raise e
    return sync_wrapper