from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.core.classes.token import Token

class UserRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, default_limits, login_limits):
        super().__init__(app)
        self.limiter = Limiter(key_func=self.get_key, default_limits=default_limits)
        self.login_limiter = Limiter(key_func=get_remote_address, default_limits=login_limits)

    async def dispatch(self, request: Request, call_next):
        # Aplicar rate limiting basado en IP para la ruta /auth/login
        if request.url.path == "/auth/login":
            client_ip = get_remote_address(request)
            try:
                self.login_limiter.check(client_ip)  # Aplica un límite estricto basado en la IP
            except Exception:
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={"detail": "Rate limit exceeded on login."},
                )

        # Aplicar rate limiting basado en user_id para rutas autenticadas
        else:
            key = self.get_key(request)
            try:
                self.limiter.check(key)  # Aplica el rate limiting normal
            except Exception:
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={"detail": "Rate limit exceeded."},
                )

        # Continuamos con la ejecución de la solicitud
        response = await call_next(request)
        return response

    def get_key(self, request: Request) -> str:
        # Para rutas autenticadas, usa el user_id del token
        authorization: str = request.headers.get("Authorization")
        if authorization:
            token_str = authorization.split(" ")[1]
            try:
                token = Token().verify_token(token=token_str)
                return token.user_id  # Usa user_id para rate limiting
            except Exception:
                pass  # En caso de fallo, podemos optar por usar la IP
        return get_remote_address(request)  # Como fallback, usa la IP