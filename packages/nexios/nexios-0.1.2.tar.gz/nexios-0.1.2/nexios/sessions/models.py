from .session_base import BaseSessionManager,AbstractBaseSession


class Session(AbstractBaseSession):
    """
    Nexio provides full support for anonymous sessions, enabling the storage and retrieval of arbitrary data on a per-visitor basis. This data is stored on the server side, while cookies are used to send and receive a session ID, rather than the data itself.

    The session framework is cookie-based and does not rely on embedding session IDs in URLs. This design choice is intentional, as it avoids the creation of ugly URLs and mitigates the risk of session ID theft through the "Referer" header.

    For detailed information on implementing sessions in your code, refer to the session documentation provided with Django 4.3 (also available on the official Django website).
    """

    objects = BaseSessionManager()

    @classmethod
    def get_session_store_class(cls):
        from nexios.sessions.backends.db import SessionStore
        return SessionStore

    class Meta:
        db_table = "nexio_session"

