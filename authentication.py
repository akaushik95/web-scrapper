from typing import Optional
from fastapi import HTTPException, Header, status

STATIC_TOKEN = "testing-token"

class Authenticator: 
    def basicAuthentication(x_token: Optional[str] = Header(None)):
        if x_token != STATIC_TOKEN:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return x_token