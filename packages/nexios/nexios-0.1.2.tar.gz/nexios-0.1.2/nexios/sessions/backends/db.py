from .base import SessionBase
from nexios.utils import timezone
import logging
from tortoise import transactions,router
from tortoise.exceptions import IntegrityError,DoesNotExist
from .exceptions import SuspiciousOperation,CreateError,DatabaseError,UpdateError
import asyncio

class SessionStore(SessionBase):

    def __init__(self,config ,session_key=None):
        super().__init__(config=config,session_key = session_key)

    @classmethod
    def get_model_class(cls):
        # Avoids a circular import and allows importing SessionStore when
        
        from nexios.sessions.models import Session


        return Session

    @property
    def model(self):
        return self.get_model_class()

    async def _get_session_from_db(self):
        
        
        try:
            return await self.model.objects.get(
                session_key=self.session_key, expire_date__gt=timezone.now()
            )
        except (DoesNotExist, SuspiciousOperation) as e:
            if isinstance(e, SuspiciousOperation):
               pass
            self._session_key = None

    async def load(self):
        s = await self._get_session_from_db()
        return self.decode(s.session_data) if s else {}

    async def exists(self, session_key):
        check = self.model.filter(session_key = session_key).exists()
        return await check

    async def create(self):
        while True:
            self._session_key = self._get_new_session_key()
            try:
                # Save immediately to ensure we have a unique entry in the
                # database.
                await self.save()
            except CreateError:
                # Key wasn't unique. Try again.
                continue
            self.modified = True
            return

    async def create_model_instance(self, data):
        """
        Return a new instance of the session model object, which represents the
        current session state. Intended to be used for saving the session data
        to the database.
        """
        session_object =  self.model.filter(session_key = self.session_key)
        self.check = session_object.exists()
        if not self.check:

            return await self.model(
                session_key= await self._get_or_create_session_key(),
                session_data=self.encode(data),
                expire_date=self.get_expiry_date(),
            )
        
        return await session_object.first().update(
            session_data=self.encode(data)

        )
    async def save(self, must_create=False): 
        """
        Save the current session data to the database. If 'must_create' is
        True, raise a database error if the saving operation doesn't create a
        new entry (as opposed to possibly updating an existing entry).
        """
        if self.session_key is None:
            return await  self.create()
        data = await self._get_session(no_load=must_create)
        obj = await self.create_model_instance(data)
        try:
            async with transactions.in_transaction():
                if not self.check:
                    await obj.save()
                else:
                    pass
        except IntegrityError:
            if must_create:
                raise CreateError
            raise
        except DatabaseError:
            if not must_create:
                raise UpdateError
            raise

    def delete(self, session_key=None):
        if session_key is None:
            if self.session_key is None:
                return
            session_key = self.session_key
        try:
            self.model.objects.get(session_key=session_key).delete()
        except self.model.DoesNotExist:
            pass

    @classmethod
    def clear_expired(cls):
        cls.get_model_class().objects.filter(expire_date__lt=timezone.now()).delete()
