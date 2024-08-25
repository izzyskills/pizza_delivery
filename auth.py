from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Union

from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from config import settings


def create_access_token(
    subject: Union[str, Any], expires_delta: int | None = None
) -> str:
    if expires_delta is not None:
        expiration_time = datetime.now(tz=timezone.utc) + timedelta(
            minutes=expires_delta
        )
    else:
        expiration_time = datetime.now(tz=timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode = {"exp": expiration_time, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, settings.algorithm)
    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any], expires_delta: int | None = None
) -> str:
    if expires_delta is not None:
        expiration_time = datetime.now(tz=timezone.utc) + timedelta(
            minutes=expires_delta
        )
    else:
        expiration_time = datetime.now(tz=timezone.utc) + timedelta(
            minutes=settings.refresh_token_expire_minutes
        )

    to_encode = {"exp": expiration_time, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.refresh_secret_key, settings.algorithm)
    return encoded_jwt


def decodeJWT(jwtoken: str):
    try:
        payload = jwt.decode(jwtoken, settings.secret_key, settings.algorithm)
        return payload
    except JWTError as e:
        print(f"JWT decode error: {str(e)}")
        return None


def decodeRefreshJWT(jwtoken: str):
    try:
        payload = jwt.decode(jwtoken, settings.refresh_secret_key, settings.algorithm)
        return payload
    except JWTError as e:
        print(f"JWT decode error: {str(e)}")
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            token = credentials.credentials
            if not self.verify_jwt(token):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return token
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> dict[str, Any] | None:
        payload = decodeJWT(jwtoken)
        return payload

    def verify_refresh_jwt(self, jwtoken: str) -> dict[str, Any] | None:
        payload = decodeRefreshJWT(jwtoken)
        return payload


jwt_bearer = JWTBearer()
