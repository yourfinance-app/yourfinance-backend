import jwt
import uuid

import yfa
from yfa.models import User, UserJWTContent

JWT_ALGO = "HS256"


def make_token(user: User):
    payload = UserJWTContent(**user.__dict__)
    return jwt.encode(
        payload={**payload.__dict__, "id": str(payload.id)},
        key=yfa.config.JWT_SECRET,
        algorithm=JWT_ALGO)


def decode_token(token: str) -> UserJWTContent:
    payload = jwt.decode(
        jwt=token,
        key=yfa.config.JWT_SECRET,
        algorithms=[JWT_ALGO]
    )
    payload["id"] = uuid.UUID(payload.get("id"))
    return UserJWTContent(**payload)
