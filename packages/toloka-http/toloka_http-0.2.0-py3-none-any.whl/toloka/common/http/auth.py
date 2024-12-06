from datetime import timedelta
from typing import Mapping, Protocol

from toloka.common.jwt.config import JwtConfig


class AuthHeaders(Protocol):
    def get_headers(self) -> Mapping[str, str]: ...


class ApiKeyHeaders(AuthHeaders):
    def __init__(self, api_key: str, key_prefix: str = 'ApiKey') -> None:
        self.api_key = api_key
        self.key_prefix = key_prefix

    def get_headers(self) -> dict[str, str]:
        api_key = self.api_key.removeprefix(f'{self.key_prefix} ')
        return {'Authorization': f'{self.key_prefix} {api_key}'}


class JWTHeaders(AuthHeaders):
    def __init__(
        self, subject: str, audience: str, secret_key: str, duration: timedelta, algorithm: str = 'HS256'
    ) -> None:
        self._subject = subject
        self._audience = audience
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._duration = duration

    def get_headers(self) -> dict[str, str]:
        token = JwtConfig(
            secret=self._secret_key,
            algorithm=self._algorithm,
            subject=self._subject,
            audience=self._audience,
            duration=self._duration,
            with_iat=True,
        ).get_token()

        return {'Authorization': f'Bearer {token}'}
