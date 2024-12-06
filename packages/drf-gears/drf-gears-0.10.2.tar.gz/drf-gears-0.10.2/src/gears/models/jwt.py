import os
import json
# import base64

from cryptography.fernet import Fernet
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


class TokenEncryption:
    @staticmethod
    def generate_salt(length: int):
        return os.urandom(length)

    @staticmethod
    def generate_key():
        return Fernet.generate_key()

    # @staticmethod
    # def k(data: dict, salt: bytes):
    #     kdf = PBKDF2HMAC(
    #         algorithm=hashes.SHA256(),
    #         length=32,
    #         salt=salt,
    #         iterations=100000,
    #         backend=default_backend(),
    #     )
    #     data = json.dumps(data).encode()
    #     return base64.urlsafe_b64encode(kdf.derive(data))

    @staticmethod
    def encrypt_data(data: dict, key: str = settings.JWT_PAYLOAD_ENCRYPTION_KEY):
        fernet = Fernet(key)
        data = json.dumps(data).encode()
        return fernet.encrypt(data)

    @staticmethod
    def decrypt_data(encrypted: bytes, key: str = settings.JWT_PAYLOAD_ENCRYPTION_KEY):
        fernet = Fernet(key)
        data = fernet.decrypt(encrypted)
        return json.loads(data)


class JWTUserModelMixin:
    def get_public_jwt_data(self) -> dict:
        """
        This method must return a payload dictionary. Fill this method with needed logic
        for building an open payload you want to put into the token.
        
        NOTICE! Be sure you do not use any sensitive data.
        JWT tokens could be unpacked by any person, so the information inside the token
        available for anyone who has this token.
        If you need to fill JWT token with a sensitive data, please use the 
        get_private_jwt_data method instead.
        
        :return: a payload dict
        """
        
        raise NotImplemented(
            "You should override this method with a specific payload builder."
        )
    
    def get_private_jwt_data(self) -> dict:
        """
        This method must return a payload dictionary. Fill this method with needed logic
        for building a sensitive data payload you want to put into the token.
        
        :return: a payload dict 
        """
        
        return {}

    def extend_token(self, token):
        """
        It takes a fresh token and extends it with an additional payload.
        There are two options: get_public_jwt_data and get_private_jwt_data. 
        :param token: a fresh valid RefreshToken
        :return: an extended RefreshToken
        """

        # Fill in the token with the public data
        public_data = self.get_public_jwt_data()
        for k, v in public_data.items():
            token[k] = v

        # Fill in the token with the private data
        private_data = self.get_private_jwt_data()
        token['private'] = TokenEncryption.encrypt_data(private_data).decode()
        return token

    def build_token(self):
        """
        It builds a RefreshToken instance and runs the extending process.
        :return: an extended RefreshToken instance
        """
        token = RefreshToken.for_user(self)
        token = self.extend_token(token)
        return token

    def get_tokens_pair(self) -> dict[str, str]:
        """
        Wrapper for the build_token method.
        :return: a dict with the access and  refresh tokens inside.
        """
        refresh = self.build_token()
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
