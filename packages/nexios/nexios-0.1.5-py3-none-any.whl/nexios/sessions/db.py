import uuid
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from .db_models import Session
from nexios.config.settings import BaseConfig
from .base import BaseSessionInterface
from nexios.utils import timezone





class DBSessionManager(BaseSessionInterface):
    def __init__(self, session_key: str, config: BaseConfig = BaseConfig):
        session_key = session_key or str(uuid.uuid4())
        super().__init__(session_key, config)
        self.session_key = session_key

    async def _load_session_data(self) -> Optional[Dict[str, Any]]:
        """Load session data from the database."""
        session = await Session.get_or_none(id=self.session_key)
        if session:
            return session.data
        return None

    async def _save_session_data(self):
        """Save the session data to the database."""
        session_data = self._session_cache
        session, created = await Session.get_or_create(id=self.session_key)
        session.data = session_data
        await session.save()

    async def set_session(self, key: str, value: str):
        """Set a session value."""
        self.modified = True
        self._session_cache[key] = value
        # Save immediately after modifying session data
        await self._save_session_data()

    async def get_session(self, key: str) -> Optional[str]:
        """Get a session value."""
        return self._session_cache.get(key, None)

    def get_all(self) -> dict:
        """Get all session data."""
        return self._session_cache.items()

    def keys(self):
        """Get all session keys."""
        return self._session_cache.keys()

    def values(self):
        """Get all session values."""
        return self._session_cache.items()

    def is_empty(self) -> bool:
        """Check if the session is empty."""
        return len(self._session_cache.items()) == 0

    async def save(self):
        """Save the session data to the database."""
        await self._save_session_data()

    @property
    def should_set_cookie(self) -> bool:
        """Determines if the cookie should be set."""
        return self.modified or (
            self.config.SESSION_PERMANENT and self.config.SESSION_REFRESH_EACH_REQUEST
        )

    def has_expired(self) -> bool:
        """Returns True if the session has expired."""
        expiration_time = self.get_expiration_time()
        if expiration_time and timezone.now() > expiration_time:
            return True
        return False

    async def load(self):
        """Load the session data from the database."""
        session_data = await self._load_session_data()
        if session_data:
            self._session_cache.update(session_data)
        else:
            self._session_cache = {}

    async def clear(self):
        """Clear the session data."""
        self._session_cache.clear()
        # Delete the session record from the database
        await Session.filter(id=self.session_key).delete()

    def get_session_key(self) -> str:
        """Returns the session key."""
        return self.session_key
