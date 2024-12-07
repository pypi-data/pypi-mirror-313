from typing import List
from fastapi import HTTPException, status
from functools import wraps

def check_roles(accepted_roles: List[str]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Obtener `config` desde los kwargs
            config = kwargs.get("config", None)

            # Verificar que `config` y `rol_code` existen
            if config is None or not hasattr(config, "rol_code"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Configuration or role code missing"
                )

            user_role = config.rol_code

            # Comprobar si el rol del usuario está en la lista de roles aceptados
            if user_role not in accepted_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"User lacks the required role: {user_role}"
                )

            # Ejecutar la función original si pasa la verificación de roles
            return await func(*args, **kwargs)

        return wrapper

    return decorator