from pydantic import BaseModel, ConfigDict


class JwtTokens(BaseModel):
    model_config = ConfigDict(frozen=True)

    access_token: str
    refresh_token: str


class DecodedJwtToken(BaseModel):
    payload: dict
    has_expired: bool
