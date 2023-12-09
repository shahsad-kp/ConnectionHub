import enum
from datetime import timedelta, datetime
from uuid import UUID

from django.conf import settings
from django.core.signing import BadSignature, loads, dumps
from django.utils import timezone
from django.contrib.auth import get_user_model

from Account.exceptions import InvalidToken, TokenExpired


class TokenTypes(enum.Enum):
    RESET_PASSWORD = '<PASSWORD>'
    LOGIN = '<LOGIN>'
    EMAIL_VERIFICATION = '<EMAIL_VERIFICATION>'


class Token:
    def __init__(
            self,
            token: str = None,
            user = None,
            token_type: TokenTypes = None,
            payload: dict = None,
            expires_in: timedelta = None
    ) -> None:
        self.token = token
        self._loaded_data = None
        self._user = None

        if self.token is None:
            if not user:
                raise ValueError('User is required')
            self.token = self._generate_token(payload, token_type, expires_in, user.id)

    def __str__(self):
        return self.token

    def __repr__(self):
        return self.token

    @staticmethod
    def _generate_token(payload: dict, token_type: TokenTypes, expires_in: timedelta, user_id: UUID):
        data = {
            'payload': payload,
            'type': str(token_type),
            'user_id': str(user_id),
            'created_at': timezone.now().isoformat(),
            'expire_at': (timezone.now() + expires_in).isoformat()
        }
        return dumps(data)

    @classmethod
    def reset_password_token(cls, user, expires_in: timedelta = timedelta(minutes=30)):
        data = {}
        return cls(payload=data, user=user, token_type=TokenTypes.RESET_PASSWORD, expires_in=expires_in)

    @classmethod
    def email_verification_token(cls, user, expires_in: timedelta = timedelta(minutes=30)):
        data = {}
        return cls(payload=data, user=user, token_type=TokenTypes.EMAIL_VERIFICATION, expires_in=expires_in)

    def verify(self):
        if self.is_expired:
            raise TokenExpired
        return False

    @property
    def _data(self) -> dict:
        if self._loaded_data is None:
            key = settings.SECRET_KEY
            try:
                self._loaded_data = loads(self.token, key=key)
            except BadSignature:
                raise InvalidToken
        return self._loaded_data

    @property
    def expire_at(self) -> timedelta:
        return self._data['expire_at']

    @property
    def is_expired(self) -> bool:
        return datetime.fromisoformat(self._data['expire_at']) < timezone.now()

    @property
    def payload(self) -> dict:
        return self._data['payload']

    @property
    def user_id(self) -> UUID:
        return self._data['user_id']

    @property
    def token_type(self) -> TokenTypes:
        return self._data['token_type']

    @property
    def expires_in(self) -> timedelta:
        return datetime.fromisoformat(self._data['expire_at']) - timezone.now()

    @property
    def user(self):
        if self._user is None:
            User = get_user_model()
            self._user = User.objects.get(pk=self.user_id)
        return self._user

    @payload.setter
    def payload(self, payload: dict):
        self.token = self._generate_token(
            payload,
            token_type=self.token_type,
            expires_in=self.expire_at,
            user_id=self.user_id
        )

    def __getitem__(self, item):
        return self.payload[item]

    def __setitem__(self, key, value):
        payload = self.payload
        payload[key] = value
        self.payload = payload
