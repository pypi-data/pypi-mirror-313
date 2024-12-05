import base64
import json
import hmac
import hashlib

class SessionEncoder:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def encode_session(self, session_data: dict) -> str:
        json_data = json.dumps(session_data)
        data = base64.b64encode(json_data.encode()).decode()
        signature = hmac.new(self.secret_key.encode(), data.encode(), hashlib.sha256).hexdigest()
        
        return f"{data}.{signature}"

    def decode_session(self, encoded_data: str) -> dict:
        data, signature = encoded_data.rsplit('.', 1)
        
        expected_signature = hmac.new(self.secret_key.encode(), data.encode(), hashlib.sha256).hexdigest()
        
        if not hmac.compare_digest(expected_signature, signature):
            raise ValueError("Invalid session data or tampering detected")
        
        json_data = base64.b64decode(data.encode()).decode()
        return json.loads(json_data)
