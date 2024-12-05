import typing
from nexios.utils import crypto
from nexios.utils import timezone
from datetime import datetime, timedelta, timezone, tzinfo
from nexios.config.settings import BaseConfig
from ..utils import SessionEncoder
from nexios.utils import timezone
import string

VALID_KEY_CHARS = string.ascii_lowercase + string.digits

class SessionBase:
    __not_given = object()
    accessed = False
    modified = False
    deleted = False
    modified_data = {}
    

    def __init__(self,
                 config = None ,
                 session_key = None ) -> None:


        self.session_key = session_key
        self.config = config
        self.modified_data :typing.Dict = {}

        try:
            secret_key = config.SECRET_KEY
        except AttributeError:
            raise AttributeError("""SECRET_KEY NOT FOUND IN YOUR CONFIG
                                 HINT :add SESSION_KEY to your config class
                                 """)
        self.signer = SessionEncoder(secret_key)
  
    def __contains__(self, key :str) -> bool:

        return key in self._session 


    async def get_session(self, key :str) -> typing.Dict[str, any]:
        self.accessed = True
        session = await self._session
        try:
            return session[key]
        except KeyError:
            return None

    

    async def set_session(self, key,value) -> None:
        session = await self._get_session()
        if key in session.keys():
            self.accessed = True
        self.modified_data.update({key:value})
        self.modified = True
    

        
    async def remove(self,key) -> None:
        session = await self._session
        del session[key]
        self.modified = True

    
    def get_salt(self) -> str:
        return "nexio.session"+self.__class__.__qualname__

    
    async def get(self, key :str) -> typing.Any:
        self.accessed = False
        session = await self._session

        return session.get(key)

    async def pop(self, key, default=__not_given):

        args = () if default is self.__not_given else (default,)
        session = await self._session
        
        return session.pop(key, *args)

    async def setdefault(self, key, value):
        session = await self._session

        self.modified = True
        if key in session:
            return session[key]
        else:
            session[key] = value
            return value

    async def update(self, dict_):
        session = await self._session

        session.update(dict_)
        self.modified = True

    async def has_key(self, key):
        session = await self._session

        return key in session

    async def keys(self):
        session = await self._session

        return session.keys()

    async def values(self):
        session = await self._session
        return  session.values()

    async def items(self):
        session = await self._session

        return session.items()

    def clear(self):
       
        self._session_cache = {}
        

    async def is_empty(self):

        try:
            return not self._session_key and not self._session_cache
        except AttributeError:
            return True

    async def _get_new_session_key(self):
        while True:
            session_key = crypto.generate_random_string(32)
            if not await self.exists(session_key):
                return session_key

    async def _get_or_create_session_key(self):
        if await self.exists(self.session_key):
            self.session_key = await self._get_new_session_key()
        if self.session_key is None:
            self.session_key = await self._get_new_session_key()
            
        return self.session_key

    def _validate_session_key(self, key):
        """
        Key must be truthy and at least 8 characters long. 8 characters is an
        arbitrary lower bound for some minimal key security.
        """
        # return key and len(key) >= 8
        return True

  

    def _set_session_key(self, value):
        """
        Validate session key on assignment. Invalid values will set to None.
        """

        if self._validate_session_key(value):
            self.__session_key = value
        else:
            self.__session_key = None

    

    async def _get_session(self, no_load=False):
        """
        Lazily load session from storage (unless "no_load" is True, when only
        an empty dict is stored) and store it in the current instance.
        """
        
        # try:
        #     return self._session_cache
        # except AttributeError:
        #     if self.session_key is None or no_load:
                
        #         self._session_cache = {}
        #     else:
                
        #         self._session_cache = self.load()
        # return self._session_cache
        if not self.modified:
            self.modified_data.update(await self.load())
        return self.modified_data

    @property
    async def _session(self):
        return await self._get_session()
    def get_session_cookie_age(self):
        return self.config.COOKIE_AGE

   

    def get_expiry_date(self, **kwargs):
        """Get session the expiry date (as a datetime object).

        Optionally, this function accepts `modification` and `expiry` keyword
        arguments specifying the modification and expiry of the session.
        """
        

        try:
            expiry = self.config.COOKIE_AGE
        except AttributeError:
            expiry = 86400
        return timezone.now() + timedelta(seconds=expiry)

    def set_expiry(self, value):
        """
        Set a custom expiration for the session. ``value`` can be an integer,
        a Python ``datetime`` or ``timedelta`` object or ``None``.

        If ``value`` is an integer, the session will expire after that many
        seconds of inactivity. If set to ``0`` then the session will expire on
        browser close.

        If ``value`` is a ``datetime`` or ``timedelta`` object, the session
        will expire at that specific future time.

        If ``value`` is ``None``, the session uses the global session expiry
        policy.
        """
        if value is None:
            # Remove any custom expiration for this session.
            try:
                del self["_session_expiry"]
            except KeyError:
                pass
            return
        if isinstance(value, timedelta):
            value = timezone.now() + value
        if isinstance(value, datetime):
            value = value.isoformat()
        self["_session_expiry"] = value

    def get_expire_at_browser_close(self):
        """
        Return ``True`` if the session is set to expire when the browser
        closes, and ``False`` if there's an expiry date. Use
        ``get_expiry_date()`` or ``get_expiry_age()`` to find the actual expiry
        date/age, if there is one.
        """
        if (expiry := self.get("_session_expiry")) is None:
            return self.config.SESSION_EXPIRE_AT_BROWSER_CLOSE
        return expiry == 0

    def flush(self):
        """
        Remove the current session data from the database and regenerate the
        key.
        """
        self.deleted = True
        self.clear()
        self.delete()
        self._session_key = None

    def cycle_key(self):
        """
        Create a new session key, while retaining the current session data.
        """
        data = self._session
        key = self.session_key
        self.create()
        self._session_cache = data
        if key:
            self.delete(key)

    # Methods that child classes must implement.

    def exists(self, session_key):
        """
        Return True if the given session_key already exists.
        """
        raise NotImplementedError(
            "subclasses of SessionBase must provide an exists() method"
        )

    def create(self):
        """
        Create a new session instance. Guaranteed to create a new object with
        a unique key and will have saved the result once (with empty data)
        before the method returns.
        """
        raise NotImplementedError(
            "subclasses of SessionBase must provide a create() method"
        )

    def save(self, must_create=False):
        """
        Save the session data. If 'must_create' is True, create a new session
        object (or raise CreateError). Otherwise, only update an existing
        object and don't create one (raise UpdateError if needed).
        """
        raise NotImplementedError(
            "subclasses of SessionBase must provide a save() method"
        )

    def delete(self, session_key=None):
        """
        Delete the session data under this key. If the key is None, use the
        current session key value.
        """
        raise NotImplementedError(
            "subclasses of SessionBase must provide a delete() method"
        )

    def load(self):
        """
        Load the session data and return a dictionary.
        """
        raise NotImplementedError(
            "subclasses of SessionBase must provide a load() method"
        )

    @classmethod
    def clear_expired(cls):
        """
        Remove expired sessions from the session store.

        If this operation isn't possible on a given backend, it should raise
        NotImplementedError. If it isn't necessary, because the backend has
        a built-in expiration mechanism, it should be a no-op.
        """
        raise NotImplementedError("This backend does not support clear_expired().")
    
    def encode(self,data):
        return self.signer.encode_session(data)
    
    def decode(self, encoded_data):
        data = self.signer.decode_session(encoded_data)
        return data
        




    






       

