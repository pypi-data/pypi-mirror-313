from .application import NexioApp 
from .sessions.middleware import SessionMiddleware
from .middlewares.logging import ErrorHandlerMiddleware
from .middlewares.common import CommonMiddleware
from .config.settings import BaseConfig
from .routers import Router
from .middlewares.cors import CORSMiddleware
import os



def get_application(config = BaseConfig) -> NexioApp:
    config=config()
    app = NexioApp(
        middlewares= [
            
            ErrorHandlerMiddleware(),
            
            CommonMiddleware(),
            CORSMiddleware(
                allow_origins=config.CORS_ALLOWED_ORIGINS,
                blacklist_origins=config.CORS_BLACKLISTED_ORIGINS,
                allow_methods=config.CORS_ALLOWED_METHODS,
                allow_credentials=config.CORS_ALLOW_CREDENTIALS,
                allow_headers=config.CORS_ALLOW_HEADERS,
                expose_headers = config.EXPOSE_HEADERS,
                allow_origin_regex=config.ALLOW_ORIGIN_REGEX
                
                
                ),
            SessionMiddleware()

        ],
        config=config
    )
    
    return app