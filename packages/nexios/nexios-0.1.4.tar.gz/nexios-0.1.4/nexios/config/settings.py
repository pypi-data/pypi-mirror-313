
from typing import Any


class BaseConfig:

    debug :bool  = False

    middlewares :list = [] 

    COOKIE_AGE = 259200


    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
            
        except AttributeError:
            return None


