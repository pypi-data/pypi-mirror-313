import typing
from nexios.config.settings import BaseConfig
from nexios.utils import timezone
from datetime import datetime
class BaseSessionInterface:

    modified = False

    accessed = False

    deleted = False

    _session_cache = {} 


    def __init__(self,
                 session_key :str,
                 config :BaseConfig = BaseConfig) -> None:
        

        self.session_key = session_key 
        assert config.SECRET_KEY != None, "Secret key is required to use session"
        self.config = config




    def set_session(self,key :str,value :str):
        self.modified = True
        self.accessed = True

        self._session_cache[key] = value
    
    def get_session(self, key):
        self.accessed = True
        
        return self._session_cache.get(key, None)
        

    def get_all(self):
        self.accessed = True
        return self._session_cache.items()
    
    def keys(self):
        return self._session_cache.keys()
    
    def values(self):
        return self._session_cache.items()
    
    def is_empty(self):
        return self._session_cache.items().__len__() == 0
    

    async def save(self):

        raise NotImplemented

    def get_cookie_name(self) -> str:
        """The name of the session cookie. Uses``app.config.SESSION_COOKIE_NAME``."""
        return self.config.SESSION_COOKIE_NAME or "session_id"

    def get_cookie_domain(self) -> str | None:
        """Returns the domain for which the cookie is valid. Uses `config.SESSION_COOKIE_DOMAIN`."""
        return self.config.SESSION_COOKIE_DOMAIN

    def get_cookie_path(self) -> str:
        """Returns the path for which the cookie is valid. Uses `config.SESSION_COOKIE_PATH`."""
        return self.config.SESSION_COOKIE_PATH

    def get_cookie_httponly(self) -> bool:
        """Returns whether the session cookie should be HTTPOnly. Uses `config.SESSION_COOKIE_HTTPONLY`."""
        return self.config.SESSION_COOKIE_HTTPONLY

    def get_cookie_secure(self) -> bool:
        """Returns whether the session cookie should be secure. Uses `config.SESSION_COOKIE_SECURE`."""
        return self.config.SESSION_COOKIE_SECURE

    def get_cookie_samesite(self) -> str | None:
        """Returns the SameSite attribute for the cookie. Uses `config.SESSION_COOKIE_SAMESITE`."""
        return self.config.SESSION_COOKIE_SAMESITE

    def get_cookie_partitioned(self) -> bool:
        """Returns whether the cookie should be partitioned. Uses `config.SESSION_COOKIE_PARTITIONED`."""
        return self.config.SESSION_COOKIE_PARTITIONED

    def get_expiration_time(self) -> datetime | None:
        """Returns the expiration time for the session. Uses `config.SESSION_EXPIRATION_TIME`."""
        if self.config.SESSION_PERMANENT:
            return timezone.now() + self.config.SESSION_EXPIRATION_TIME or 86400
        return None

    @property
    def should_set_cookie(self) -> bool:
        """Determines if the cookie should be set. Depends on `config.SESSION_REFRESH_EACH_REQUEST`."""
        return self.modified or (
            self.config.SESSION_PERMANENT and self.config.SESSION_REFRESH_EACH_REQUEST
        )

    def has_expired(self) -> bool:
        """Returns True if the session has expired."""
        expiration_time = self.get_expiration_time()
        if expiration_time and timezone.now() > expiration_time:
            return True
        return False
