import enum

from pydantic import BaseModel


class JwtAlgorithm(str, enum.Enum):
    hs256 = "HS256"


class JwtSettings(BaseModel):
    access_secret_key: str
    refresh_secret_key: str
    access_token_lifetime_seconds: int = 5 * 60  # 5 min
    refresh_token_lifetime_seconds: int = 60 * 60 * 24 * 7  # 7 days
    algorithm: JwtAlgorithm = JwtAlgorithm.hs256
