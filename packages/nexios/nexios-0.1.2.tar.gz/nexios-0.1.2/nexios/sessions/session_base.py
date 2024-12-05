try:
    import tortoise
    import aerich

except ImportError:
    raise ImportError("Tortoise orm and aerich no installed")


from   tortoise import Model,fields,manager


class BaseSessionManager(manager.Manager):
    def encode(self, session_dict):
        """
        Return the given session dictionary serialized and encoded as a string.
        """
        session_store_class = self.model.get_session_store_class()
        return session_store_class().encode(session_dict)

    def save(self, session_key, session_dict, expire_date):
        s = self.model(session_key, self.encode(session_dict), expire_date)
        if session_dict:
            s.save()
        else:
            s.delete()  # Clear sessions with no data.
        return s

class AbstractBaseSession(Model):
    session_key = fields.CharField( max_length=240, primary_key=True)

    #session_key can be assumed to be a hmac_hash
    session_data = fields.TextField()
    expire_date = fields.DatetimeField(db_index=True)

    objects = BaseSessionManager()

    # class Meta:
    #     abstract = True

    def __str__(self):
        return self.session_key

    @classmethod
    def get_session_store_class(cls):
        raise NotImplementedError

    def get_decoded(self):
        session_store_class = self.get_session_store_class()
        return session_store_class().decode(self.session_data)

    class Meta:
        abstract = True
