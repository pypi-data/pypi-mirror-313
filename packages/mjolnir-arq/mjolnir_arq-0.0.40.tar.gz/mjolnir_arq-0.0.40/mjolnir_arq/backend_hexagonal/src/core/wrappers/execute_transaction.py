import json
from functools import wraps
from fastapi import HTTPException
from termcolor import colored
import traceback


def execute_transaction(layer, enabled=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not enabled:
                # Si el decorador está deshabilitado, simplemente ejecuta la función original
                return func(*args, **kwargs)
            try:
                # Ejecutar la función original
                return func(*args, **kwargs)
            except Exception as e:
                # Obtener la clase y el nombre del método
                class_name = func.__qualname__.split(".")[0]
                method_name = func.__name__

                # Extraer los parámetros `params` y `config`
                params = kwargs.get("params", args[1] if len(args) > 1 else None)
                config = kwargs.get("config", args[0] if len(args) > 0 else None)

                # Preparar los datos de los parámetros
                params_data = {}
                if params:
                    try:
                        if hasattr(params, "dict"):
                            params_data = params.dict()
                        elif hasattr(params, "__dict__"):
                            params_data = params.__dict__
                        else:
                            params_data = str(params)
                    except Exception as ex:
                        params_data = f"Unserializable params: {ex}"

                config_data = {}
                if config:
                    try:
                        if hasattr(config, "dict"):
                            config_data = config.dict()
                        elif hasattr(config, "__dict__"):
                            config_data = {
                                k: (
                                    str(v)
                                    if not isinstance(
                                        v,
                                        (dict, list, str, int, float, bool, type(None)),
                                    )
                                    else v
                                )
                                for k, v in config.__dict__.items()
                            }
                        else:
                            config_data = str(config)
                    except Exception as ex:
                        config_data = f"Unserializable config: {ex}"

                # Capturar la traza del error
                tb = traceback.extract_tb(e.__traceback__)
                filename = tb[-1].filename
                line_number = tb[-1].lineno

                # Formatear y retornar los datos de error
                error_data = {
                    "layer": layer,
                    "class_name": class_name,
                    "method_name": method_name,
                    "params": params_data,
                    "config": config_data,
                    "error": str(e).replace("500:", "").lstrip(),
                    "file": filename,
                    "line": line_number,
                }

                # Serializar el diccionario a JSON
                error_json = json.dumps(error_data, indent=4, default=str)

                # Imprimir el error formateado
                print(
                    colored(
                        f"ERROR: {error_json}",
                        "light_red",
                    )
                )
                print(
                    colored(
                        "-" * 100,
                        "light_red",
                    )
                )

                # Lanzar una excepción HTTP con el mensaje de error
                raise HTTPException(
                    status_code=500, detail=f"{e}".replace("500:", "").lstrip()
                )

        return wrapper

    return decorator


def string_to_json(text: str):
    try:
        # Remover caracteres de escape como '\n' y otros
        cleaned_text = text.replace("\\n", "").replace("\\t", "").replace("\\", "")

        # Intentar convertir la cadena en un objeto JSON
        json_object = json.loads(cleaned_text)

        return json_object
    except json.JSONDecodeError as e:
        """ print(f"Error al convertir la cadena a JSON: {e}") """
        return None


def execute_transaction_route(enabled=True):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not enabled:
                # Si el decorador está deshabilitado, simplemente ejecuta la función original
                return await func(*args, **kwargs)

            try:
                # Obtener `config` desde los kwargs
                config = kwargs.get("config", None)

                if config is not None and hasattr(config, "request"):
                    request = config.request
                else:
                    request = None

                if request:
                    body = await request.body()
                    formatted_body = (
                        body.decode("utf-8") if isinstance(body, bytes) else str(body)
                    )

                    json_body = string_to_json(formatted_body)

                    # Almacenar directamente el objeto JSON si es válido
                    request.state.body = (
                        json_body if json_body is not None else formatted_body
                    )

                return await func(*args, **kwargs)
            except Exception as e:
                route_info = {}

                if request and hasattr(request.state, "body"):
                    body_content = request.state.body

                    x_forwarded_for = request.headers.get("X-Forwarded-For")
                    if x_forwarded_for:
                        client_ip = x_forwarded_for.split(",")[0]
                    else:
                        client_ip = request.client.host

                    route_info = {
                        "method": request.method,
                        "url": str(request.url),
                        "path": request.url.path,
                        "query_params": dict(request.query_params),
                        "headers": dict(request.headers),
                        "ip": client_ip,
                    }

                    if isinstance(body_content, dict):
                        route_info["json_body"] = body_content
                    else:
                        route_info["body"] = body_content
                else:
                    route_info = {
                        "method": "unknown",
                        "url": "unknown",
                        "path": "unknown",
                        "query_params": {},
                        "headers": {},
                        "body": "No request data available",
                    }

                error_info = {
                    "error": f"{e}".replace("500:", "").lstrip(),
                    "route_info": route_info,
                }

                print(
                    colored(
                        f"ERROR: {json.dumps(error_info, indent=4)}",
                        "light_red",
                    )
                )

                print(
                    colored(
                        "-" * 100,
                        "light_red",
                    )
                )
                raise HTTPException(
                    status_code=500, detail=f"{e}".replace("500:", "").lstrip()
                )

        return wrapper

    return decorator
