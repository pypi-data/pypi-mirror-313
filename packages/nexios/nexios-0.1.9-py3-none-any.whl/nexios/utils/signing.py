import json
import warnings
import hashlib
import hmac
import base64
import typing
def xor_encrypt_decrypt(data, key):
    # Convert data to bytes, and key to byte format
    data_bytes = bytearray(data, 'utf-8')
    key_bytes = bytearray(key, 'utf-8')
    
    encrypted_decrypted_data = bytearray()
    
    for i in range(len(data_bytes)):
        encrypted_decrypted_data.append(data_bytes[i] ^ key_bytes[i % len(key_bytes)])
    
    return bytes(encrypted_decrypted_data)

class JSONSerializer:
    """
    Simple wrapper around json to be used in signing.dumps and
    signing.loads.
    """

    @classmethod
    def dumps(self, obj :typing.Dict[str, any]) -> str:
        return json.dumps(obj, separators=(",", ":")).encode("latin-1")

    @classmethod
    def loads(self, data :str) -> typing.Dict[str, any]:
        return json.loads(data.decode("latin-1"))

def dumps(secret_key :str,
          data :str
          ):
    
    serialized_data = JSONSerializer.dumps()


def loads(
    s,
    key=None,
    salt="django.core.signing",
    serializer=JSONSerializer,
    max_age=None,
    fallback_keys=None,
):
    """
    Reverse of dumps(), raise BadSignature if signature fails.

    The serializer is expected to accept a bytestring.
    """
    return TimestampSigner(
        key=key, salt=salt, fallback_keys=fallback_keys
    ).unsign_object(
        s,
        serializer=serializer,
        max_age=max_age,
    )

class TimestampSigner(Signer):
    def timestamp(self):
        return b62_encode(int(time.time()))

    def sign(self, value):
        value = "%s%s%s" % (value, self.sep, self.timestamp())
        return super().sign(value)

    def unsign(self, value, max_age=None):
        """
        Retrieve original value and check it wasn't signed more
        than max_age seconds ago.
        """
        result = super().unsign(value)
        value, timestamp = result.rsplit(self.sep, 1)
        timestamp = b62_decode(timestamp)
        if max_age is not None:
            if isinstance(max_age, datetime.timedelta):
                max_age = max_age.total_seconds()
            # Check timestamp is not older than max_age
            age = time.time() - timestamp
            if age > max_age:
                raise SignatureExpired("Signature age %s > %s seconds" % (age, max_age))
        return value
