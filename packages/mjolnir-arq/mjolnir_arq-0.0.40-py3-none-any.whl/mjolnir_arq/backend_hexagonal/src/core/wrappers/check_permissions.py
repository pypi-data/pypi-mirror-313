from functools import wraps
from typing import List
from fastapi import HTTPException, status

def check_permissions(accepted_permissions: List[str]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Obtener `config` desde los kwargs
            config = kwargs.get("config", None)

            # Verificar que `config` y `token` existen
            if config is None or not hasattr(config, "token"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Configuration or token missing"
                )

            token = config.token

            # Verificar si el token tiene permisos
            if not hasattr(token, "permissions"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Token does not contain permissions"
                )

            # Extraer permisos del token
            user_permissions = [perm for perm in token.permissions]

            # Buscar los permisos que faltan
            missing_permissions = [
                perm for perm in accepted_permissions if perm not in user_permissions
            ]

            # Si faltan permisos, generar una excepción con el detalle de qué permisos faltan
            if missing_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"User lacks the following required permissions: {', '.join(missing_permissions)}"
                )
            

            # Ejecutar la función original si pasa las verificaciones de permisos
            return await func(*args, **kwargs)

        return wrapper

    return decorator