from datetime import datetime, UTC, timedelta
from typing import List

from jwt import decode, encode, DecodeError

from ultra_framework.models.user import UserModel
from ultra_framework.utils.exceptions import JWTException


class RolesUtils:

    @staticmethod
    def serialize(roles: List[str]) -> str:
        return ";".join(roles)

    @staticmethod
    def deserialize(roles_str: str) -> List[str]:
        return roles_str.split(";")


class JWTHandler:

    token_alg: str = "HS256"
    datetime_fmt: str = "%Y-%m-%d %H:%M:%S"

    def __init__(self, token_key: str):
        self.token_key = token_key

    def decode_token(self, token: str) -> UserModel:

        if token is None or len(token) == 0:
            raise JWTException("Token not provided.")

        try:
            payload: dict = decode(token, self.token_key,
                                   algorithms=[self.token_alg])
            name: str | None = payload.get("name", None)
            sub: str | None = payload.get("sub", None)
            roles: List[str] = RolesUtils.deserialize(payload.get("roles", ""))
            expires_at: datetime = datetime.strptime(payload.get("expires_at"), self.datetime_fmt)
        except DecodeError as exc:
            raise JWTException("Invalid token.") from exc

        if sub is None:
            raise JWTException("Invalid credentials.")

        if expires_at < datetime.now(UTC):
            raise JWTException("Token expired.")

        return UserModel(name=name, email=sub, roles=roles)

    def encode_token(self, user: UserModel,
                     expire_minutes: int = 15) -> str:
        expires_dt = datetime.now(UTC) + timedelta(minutes=expire_minutes)
        payload = {
            "name": user.name,
            "sub": user.email,
            "roles": RolesUtils.serialize(user.roles),
            "expires_at": expires_dt.strftime(self.datetime_fmt)
        }
        access_token = encode(payload, self.token_key, self.token_alg)
        return access_token
