from fastapi.security import HTTPBearer
from fastapi import HTTPException, Path, Query, Request, Depends
from fastapi.security.http import HTTPAuthorizationCredentials

from src.core.classes.token import Token
 

 
 
class Bearer(HTTPBearer):
    def __init__(
        self,
    ):
        super().__init__()
        self.token = Token()
 
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        auth = await super().__call__(request)
        data = self.tokenManager.verify_token(auth.credentials)
        if not data:
            raise HTTPException(
                status_code=401,
                detail={
                    "error": "Unauthorized",
                    "message": "Token is invalid or expired"
                }
            )
        return auth