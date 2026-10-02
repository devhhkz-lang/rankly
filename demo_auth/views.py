import secrets
import time
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.security import APIKeyHeader, HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix="/demo-auth")


# ---------- 1. Basic Auth ----------
security = HTTPBasic()

users = {
    "admin": "admin",
    "Dulat": "12345",
}


def auth(creds: Annotated[HTTPBasicCredentials, Depends(security)]) -> str:
    if (expected := users.get(creds.username)) and secrets.compare_digest(
        creds.password.encode(), expected.encode()
    ):
        return creds.username
    
    raise HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "Invalid credentials",
        headers={"WWW-Authenticate": "Basic"},
    )


@router.get("/basic-welcome")
def welcome_username(username: Annotated[str, Depends(auth)]) -> dict:
    return {"message": f"Hello, {username}!", "username": username}

