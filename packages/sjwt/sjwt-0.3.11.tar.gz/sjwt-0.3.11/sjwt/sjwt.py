import base64
import hmac
import hashlib
import json
from datetime import datetime


class Token:
    def encode_array(self, array: dict) -> str:
        url = json.dumps(array)
        url_bytes = url.encode('utf-8')
        encoded = base64.b64encode(url_bytes)
        return encoded

    def encode_headers_payloads(self) -> None:
        self.encode_headers = self.encode_array(self.headers)
        self.encode_payload = self.encode_array(self.payload)
        return None

    def decode_string(self) -> dict:
        data = base64.b64decode(self.encode_payload)
        res = json.loads(data.decode('utf-8'))
        return res

    def get_sign(self) -> str:
        key = self.key.encode('utf-8')
        source = self.encode_headers + self.encode_payload
        sign = hmac.new(key, source, hashlib.sha256)
        return sign.hexdigest()


class TokenGet(Token):
    def __init__(self):
        self.headers = {"alg": "HS256", "typ": "JWT"}
        self.payload = {}

    def get_token(self, key: str, ttl=3600, **payload) -> str:
        self.payload['iat'] = datetime.now().timestamp()
        for k, value in payload.items():
            self.payload[k] = value
        self.payload['exp'] = self.payload['iat'] + ttl
        self.encode_headers_payloads()
        self.key = key
        sign = self.get_sign()
        return self.encode_headers.decode('utf-8') + '.' + self.encode_payload.decode('utf-8') + '.' + sign


class TokenCheck(Token):
    def __init__(self):
        self.payload = {}

    def get_sign_for_check(self) -> str:
        key = self.key.encode('utf-8')
        source = (self.encode_headers + self.encode_payload).encode('utf-8')
        sign = hmac.new(key, source, hashlib.sha256)
        return sign.hexdigest()

    def check_token(self, **kwargs) -> bool:
        self.token = kwargs['token']
        self.key = kwargs['key']
        try:
            token_list = self.token.strip().split('.')
            self.encode_headers = token_list[0]
            self.encode_payload = token_list[1]
            self.sign = token_list[2]
        except Exception:
            self.encode_headers = False
            self.encode_payload = False
        current_time = datetime.now().timestamp()
        try:
            sign = self.get_sign_for_check()
            payload = self.decode_string()
            if sign != self.sign:
                return False
            if payload['exp'] <= current_time:
                return False
            if current_time < payload['iat']:
                return False
            return True
        except Exception:
            return False

    def get_payload(self, **kwargs) -> dict:
        self.token = kwargs['token']
        self.key = kwargs['key']
        try:
            check = self.check_token(**kwargs)
            result = self.decode_string()
            result["Check_token"] = check
            return result
        except Exception:
            return "Token can broken"


gettoken = TokenGet()
checktoken = TokenCheck()
