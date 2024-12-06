import jwt
from injector import inject, singleton
from jwt import DecodeError

from griff.services.abstract_service import AbstractService
from griff.services.date.date_service import DateService
from griff.services.jwt.jwt_models import DecodedJwtToken, JwtTokens
from griff.services.jwt.jwt_settings import JwtSettings
from griff.utils.exceptions import UnauthorizedException


class InvalidTokenException(UnauthorizedException):
    default_message = "Invalid token, impossible to check"


@singleton
class JwtService(AbstractService):
    @inject
    def __init__(self, settings: JwtSettings, date_service: DateService):
        self._settings = settings
        self._algorithm = self._settings.algorithm.value
        self._date_service = date_service

    def create_jwt_tokens(self, payload: dict, ts: float | None = None) -> JwtTokens:
        if ts is None:
            ts = self._date_service.now().to_timestamp()

        access_token = self._create_access_token(payload, ts)
        refresh_token = self._create_refresh_token(payload, ts)

        return JwtTokens(access_token=access_token, refresh_token=refresh_token)

    def decode_access_token(self, access_token: str) -> DecodedJwtToken:
        return self._decode_token(access_token, self._settings.access_secret_key)

    def decode_refresh_token(self, refresh_token: str) -> DecodedJwtToken:
        return self._decode_token(refresh_token, self._settings.refresh_secret_key)

    def _create_access_token(self, payload: dict, ts: float) -> str:
        prepared_payload = self._prepare_payload(
            payload, ts, self._settings.access_token_lifetime_seconds
        )
        return jwt.encode(
            prepared_payload,
            self._settings.access_secret_key,
            algorithm=self._algorithm,
        )

    def _create_refresh_token(self, payload: dict, ts: float) -> str:
        prepared_payload = self._prepare_payload(
            payload, ts, self._settings.refresh_token_lifetime_seconds
        )
        return jwt.encode(
            prepared_payload,
            self._settings.refresh_secret_key,
            algorithm=self._algorithm,
        )

    def _decode_token(self, token: str, secret_key: str) -> DecodedJwtToken:
        try:
            decoded_token = jwt.decode(token, secret_key, algorithms=[self._algorithm])
        except DecodeError:
            raise InvalidTokenException()

        token_expires_ts = decoded_token.pop("expires", 0)
        now_ts = self._date_service.now().to_timestamp()
        has_expired = token_expires_ts < now_ts
        return DecodedJwtToken(payload=decoded_token, has_expired=has_expired)

    @staticmethod
    def _prepare_payload(payload: dict, ts: float, token_lifetime: int):
        return {**payload, "expires": ts + token_lifetime}
