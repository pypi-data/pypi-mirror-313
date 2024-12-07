import os
import shutil
from typing import Any, List
from termcolor import colored
from sqlalchemy import BOOLEAN, TIMESTAMP, UUID, VARCHAR, INTEGER, FLOAT, TEXT
from InquirerPy import inquirer
from mjolnir_arq.core.databases.connection_postgresql import ConnectionPostgresql
from mjolnir_arq.core.methods.methods import (
    convert_to_kebab_case,
    execute_commands_in_directory,
    snake_to_pascal,
)
from mjolnir_arq.core.models.directory_manager import DirectoryManager
from mjolnir_arq.core.models.file_manager import FileManager
from mjolnir_arq.core.models.login_db import LoginDB
import importlib.resources as pkg_resources


def check_folder_exists_os(folder_path):
    return os.path.isdir(folder_path)


def get_current_directory():
    return os.getcwd()


class MjolnirBusiness:

    def __init__(self) -> None:
        self.db = None
        self.current_directory = get_current_directory()
        self.directory_manager = DirectoryManager()
        self.file_manager = FileManager()

    def copy_all_contents(self, origen, destino):
        # Verificar si el directorio de destino existe, si no, crearlo
        if not os.path.exists(destino):
            os.makedirs(destino)

        # Usar shutil.copytree con dirs_exist_ok=True para copiar todo
        shutil.copytree(origen, destino, dirs_exist_ok=True)

    def create_project(self) -> None:
        try:
            # Obtener la ruta al directorio 'backend_hexagonal'
            origen = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "backend_hexagonal"
            )
            destino = self.current_directory

            # Si el directorio de destino no existe, crear el directorio
            if not os.path.exists(destino):
                os.makedirs(destino)
                print(colored(f"SUCCESS: Directorio de destino creado.", "cyan"))

            # Copiar el contenido del directorio origen al destino
            self.copy_all_contents(origen, destino)
            print(colored(f"Cargando...", "cyan"))

            # Ejecutar comandos en el directorio destino
            execute_commands_in_directory(
                comandos=[
                    "python3.11 -m venv env",
                    "source env/bin/activate",
                    "pip install -r pipfiles.txt",
                ],
                directorio_destino=destino,
            )
            print(colored(f"SUCCESS: Entorno virtual creado.", "cyan"))
            print(colored(f"SUCCESS: Librerías instaladas.", "cyan"))
            print(colored(f"SUCCESS: Proyecto creado.", "cyan"))
            print(colored(f"----------------------------------------", "cyan"))
            print(
                colored(
                    f"NOTA: 1. Debes correr la migracion v1 que esta en la carpeta de migraciones en tu base de datos. [postgresql]",
                    "cyan",
                )
            )
            print(
                colored(
                    f"NOTA: 2. Debes ajustar tus credenciales de base de datos en los archivos .env",
                    "cyan",
                )
            )
            print(
                colored(
                    f"NOTA: 3. Debes ajustar el puerto donde correra tu microservicio en los diferentes ambientes\n valida los archivos Dockerfile y docker-compose.",
                    "cyan",
                )
            )
            print(
                colored(
                    f"NOTA: 4. Corre la libreria [escribe <mj> para inicializar la libreria] y crea el primer flujo base",
                    "cyan",
                )
            )
            print(
                colored(
                    f"NOTA: 4.1 Cuando te pida la consola -> Introduce nombre de la tabla: ingresa: language",
                    "cyan",
                )
            )
            print(
                colored(
                    f"NOTA: 5. Corre la libreria [escribe <mj> para inicializar la libreria] y crea el segundo flujo base",
                    "cyan",
                )
            )
            print(
                colored(
                    f"NOTA: 5.1 Cuando te pida la consola -> Introduce nombre de la tabla: ingresa: translation",
                    "cyan",
                )
            )
            print(
                colored(
                    f"NOTA FINAL: Completando los pasos puedes ejecutar el microservicio",
                    "cyan",
                )
            )

        except Exception as e:
            print(
                colored(
                    f"ERROR: No se pudo crear el proyecto. {e}",
                    "light_red",
                )
            )

    def data_connection_db(self):
        name_db = inquirer.text(
            message="Introduce nombre de la base de datos:"
        ).execute()
        name_user = inquirer.text(message="Introduce nombre de usuario:").execute()
        password = inquirer.text(message="Introduce la contraseña:").execute()
        port = inquirer.text(message="Introduce el puerto:").execute()
        host = inquirer.text(message="Introduce host:").execute()
        scheme = inquirer.text(message="Introduce el esquema:").execute()

        return LoginDB(
            name_db=name_db,
            name_user=name_user,
            password=password,
            port=port,
            host=host,
            scheme=scheme,
        )

        """ return LoginDB(
            name_db="platform_qa",
            name_user="postgres",
            password="marlon",
            port="5432",
            host="localhost",
        ) """

    def create_flow_base_complete(self):
        self.db = ConnectionPostgresql(loginDB=self.data_connection_db())

        table_names = self.db.inspector.get_table_names()
         

        for name_table in table_names:
            result = self.validate_name_table(name_table=name_table)
            if not result:
                return

            result = self.domain_models_entities(name_table=name_table)
            if not result:
                return

            result = self.domain_services_repositories_entities(name_table=name_table)
            if not result:
                return

            result = self.domain_services_use_cases_entities(name_table=name_table)
            if not result:
                return

            result = self.infrastructure_database_entities(name_table=name_table)
            if not result:
                return

            result = self.infrastructure_database_mappers(name_table=name_table)
            if not result:
                return

            result = self.infrastructure_database_repositories(name_table=name_table)
            if not result:
                return

            result = self.infrastructure_web_controller_entities(name_table=name_table)
            if not result:
                return

            result = self.infrastructure_web_entities_routes(name_table=name_table)
            if not result:
                return

            result = self.infrastructure_web_routes(name_table=name_table)
            if not result:
                return
            print(colored(".", "cyan") * 100)

    def create_flow_base(self):
        self.db = ConnectionPostgresql(loginDB=self.data_connection_db())
        name_table = inquirer.text(message="Introduce nombre de la tabla:").execute()

        result = self.validate_name_table(name_table=name_table)
        if not result:
            return

        result = self.domain_models_entities(name_table=name_table)
        if not result:
            return

        result = self.domain_services_repositories_entities(name_table=name_table)
        if not result:
            return

        result = self.domain_services_use_cases_entities(name_table=name_table)
        if not result:
            return

        result = self.infrastructure_database_entities(name_table=name_table)
        if not result:
            return

        result = self.infrastructure_database_mappers(name_table=name_table)
        if not result:
            return

        result = self.infrastructure_database_repositories(name_table=name_table)
        if not result:
            return

        result = self.infrastructure_web_controller_entities(name_table=name_table)
        if not result:
            return

        result = self.infrastructure_web_entities_routes(name_table=name_table)
        if not result:
            return

        result = self.infrastructure_web_routes(name_table=name_table)
        if not result:
            return

    def domain_models_entities(self, name_table: str) -> bool:
        base_path = os.path.join(
            self.current_directory, "src", "domain", "models", "entities", name_table
        )
        if not self.directory_exists(folder_path=base_path):
            return False
        self.directory_manager.create_directory(dir_path=base_path)

        file_contents: dict[str, str] = {
            f"{name_table}.py": self.create_entity_base(name_table=name_table),
            f"{name_table}_save.py": self.create_entity_save(name_table=name_table),
            f"{name_table}_read.py": self.create_entity_read(name_table=name_table),
            f"{name_table}_delete.py": self.create_entity_delete(name_table=name_table),
            f"{name_table}_update.py": self.create_entity_update(name_table=name_table),
            f"index.py": self.domain_models_entities_index(name_table=name_table),
            "__init__.py": "",
        }

        for file_name, content in file_contents.items():
            file_path = os.path.join(base_path, file_name)
            self.file_manager.create_file(file_path=file_path, content=content)

        return True

    def domain_models_entities_index(self, name_table: str):
        pascal_name_table = snake_to_pascal(snake_str=name_table)
        model_code = f"""
from .{name_table} import {pascal_name_table}
from .{name_table}_delete import {pascal_name_table}Delete
from .{name_table}_read import {pascal_name_table}Read
from .{name_table}_save import {pascal_name_table}Save
from .{name_table}_update import {pascal_name_table}Update

__all__ = [
    "{pascal_name_table}",
    "{pascal_name_table}Delete",
    "{pascal_name_table}Read",
    "{pascal_name_table}Save",
    "{pascal_name_table}Update",
]
        """
        return model_code

    def domain_services_repositories_entities(self, name_table: str) -> bool:
        base_path = os.path.join(
            self.current_directory,
            "src",
            "domain",
            "services",
            "repositories",
            "entities",
        )
        if not self.file_exists(file_path=f"{base_path}/i_{name_table}_repository.py"):
            return False

        file_contents: dict[str, str] = {
            f"i_{name_table}_repository.py": self.create_domain_services_repositories_entities(
                name_table=name_table
            )
        }

        for file_name, content in file_contents.items():
            file_path = os.path.join(base_path, file_name)
            self.file_manager.create_file(file_path=file_path, content=content)

        return True

    def domain_services_use_cases_entities(self, name_table: str) -> bool:
        base_path = os.path.join(
            self.current_directory,
            "src",
            "domain",
            "services",
            "use_cases",
            "entities",
        )
        if not self.directory_exists(folder_path=f"{base_path}/{name_table}"):
            return False

        self.directory_manager.create_directory(dir_path=f"{base_path}/{name_table}")

        file_contents: dict[str, str] = {
            f"{name_table}_delete_use_case.py": self.create_domain_services_use_cases_entities_delete(
                name_table=name_table
            ),
            f"{name_table}_list_use_case.py": self.create_domain_services_use_cases_entities_list(
                name_table=name_table
            ),
            f"{name_table}_read_use_case.py": self.create_domain_services_use_cases_entities_read(
                name_table=name_table
            ),
            f"{name_table}_save_use_case.py": self.create_domain_services_use_cases_entities_save(
                name_table=name_table
            ),
            f"{name_table}_update_use_case.py": self.create_domain_services_use_cases_entities_update(
                name_table=name_table
            ),
            "index.py": self.create_domain_services_use_cases_entities_index(
                name_table=name_table
            ),
            "__init__.py": "",
        }

        for file_name, content in file_contents.items():
            file_path = os.path.join(f"{base_path}/{name_table}", file_name)
            self.file_manager.create_file(file_path=file_path, content=content)

        return True

    def validate_name_table(self, name_table: str):
        table_names = self.db.inspector.get_table_names()
        if not name_table in table_names:
            print(
                colored(
                    "ERROR: 000 Ejecución no completada - nombre de la tabla no existe",
                    "light_red",
                )
            )
            return False
        return True

    def directory_exists(self, folder_path: str):

        directory_exists = self.directory_manager.directory_exists(dir_path=folder_path)

        if directory_exists:
            print(
                colored(
                    "ERROR: 001 Ejecución no completada - base ya existe en la arquitectura",
                    "light_red",
                )
            )
            return False
        return True

    def file_exists(self, file_path: str):

        directory_exists = self.file_manager.file_exists(file_path=file_path)

        if directory_exists:
            print(
                colored(
                    f"ERROR: 002 Ejecución no completada - archivo {file_path} ya existe en la arquitectura",
                    "light_red",
                )
            )
            return False
        return True

    def create_directory(self, folder_path: str):
        self.directory_manager.create_directory(dir_path=folder_path)

    def map_column_type(self, postgres_type):
        type_mapping = {
            "UUID": "UUID(as_uuid=True)",
            "VARCHAR": "String",
            "BOOLEAN": "Boolean",
            "TIMESTAMP": "DateTime",
            "INTEGER": "Integer",
            "FLOAT": "Float",
            "NUMERIC": "Float",
            "TEXT": "Text",
            "TIME": "Time",
        }
        postgres_type_str = str(postgres_type)
        for postgres, sqlalchemy in type_mapping.items():
            if postgres in postgres_type_str:
                return postgres_type_str.replace(postgres, sqlalchemy)
        return postgres_type_str

    def infrastructure_database_repositories(self, name_table: str):
        pascal_name_table = snake_to_pascal(snake_str=name_table)
        base_path = os.path.join(
            self.current_directory,
            "src",
            "infrastructure",
            "database",
            "repositories",
            "entities",
        )
        if not self.file_exists(file_path=f"{base_path}/{name_table}_repository.py"):
            return False

        model_code = f"""
from pydantic import UUID4
from datetime import datetime
from typing import List, Union
from src.core.config import settings
from sqlalchemy.future import select
from src.core.enums.layer import LAYER
from src.core.models.config import Config
from src.core.models.filter import Pagination
from src.core.methods.get_filter import get_filter
from src.core.wrappers.execute_transaction import execute_transaction
from src.domain.models.entities.{name_table}.index import (
    {pascal_name_table},
    {pascal_name_table}Delete,
    {pascal_name_table}Read,
    {pascal_name_table}Update,
)
from src.domain.services.repositories.entities.i_{name_table}_repository import (
    I{pascal_name_table}Repository,
)
from src.infrastructure.database.entities.{name_table}_entity import {pascal_name_table}Entity
from src.infrastructure.database.mappers.{name_table}_mapper import (
    map_to_{name_table},
    map_to_list_{name_table},
)


class {pascal_name_table}Repository(I{pascal_name_table}Repository):

    @execute_transaction(layer=LAYER.I_D_R.value, enabled=settings.has_track)
    async def save(self, config: Config, params: {pascal_name_table}Entity) -> Union[{pascal_name_table}, None]:
        async with config.async_db as db:
            db.add(params)
            await db.commit()
            await db.refresh(params)
            return map_to_{name_table}(params)

    @execute_transaction(layer=LAYER.I_D_R.value, enabled=settings.has_track)
    async def update(self, config: Config, params: {pascal_name_table}Update) -> Union[{pascal_name_table}, None]:
        async with config.async_db as db:
            stmt = select({pascal_name_table}Entity).filter({pascal_name_table}Entity.id == params.id)
            stmt.updated_date = datetime.now()
            result = await db.execute(stmt)
            {name_table} = result.scalars().first()

            if not {name_table}:
                return None

            update_data = params.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr({name_table}, key, value)

            await db.commit()
            await db.refresh({name_table})
            return map_to_{name_table}({name_table})

    @execute_transaction(layer=LAYER.I_D_R.value, enabled=settings.has_track)
    async def list(self, config: Config, params: Pagination) -> Union[List[{pascal_name_table}], None]:
        async with config.async_db as db:
            stmt = select({pascal_name_table}Entity)

            if params.filters:
                stmt = get_filter(
                    query=stmt, filters=params.filters, entity={pascal_name_table}Entity
                )

            if not params.all_data:
                stmt = stmt.offset(params.skip).limit(params.limit)

            result = await db.execute(stmt)
            {name_table}s = result.scalars().all()

            if not {name_table}s:
                return None
            return map_to_list_{name_table}({name_table}s)

    @execute_transaction(layer=LAYER.I_D_R.value, enabled=settings.has_track)
    async def delete(
        self,
        config: Config,
        params: {pascal_name_table}Delete,
    ) -> Union[{pascal_name_table}, None]:
        async with config.async_db as db:
            stmt = select({pascal_name_table}Entity).filter({pascal_name_table}Entity.id == params.id)
            result = await db.execute(stmt)
            {name_table} = result.scalars().first()

            if not {name_table}:
                return None

            await db.delete({name_table})
            await db.commit()
            return map_to_{name_table}({name_table})

    @execute_transaction(layer=LAYER.I_D_R.value, enabled=settings.has_track)
    async def read(
        self,
        config: Config,
        params: {pascal_name_table}Read,
    ) -> Union[{pascal_name_table}, None]:
        async with config.async_db as db:
            stmt = select({pascal_name_table}Entity).filter({pascal_name_table}Entity.id == params.id)
            result = await db.execute(stmt)
            {name_table} = result.scalars().first()

            if not {name_table}:
                return None

            return map_to_{name_table}({name_table})
        """

        file_contents: dict[str, str] = {f"{name_table}_repository.py": model_code}

        for file_name, content in file_contents.items():
            file_path = os.path.join(base_path, file_name)
            self.file_manager.create_file(file_path=file_path, content=content)

        return True

    def infrastructure_web_controller_entities(self, name_table: str):
        pascal_name_table = snake_to_pascal(snake_str=name_table)
        base_path = os.path.join(
            self.current_directory,
            "src",
            "infrastructure",
            "web",
            "controller",
            "entities",
        )
        if not self.file_exists(file_path=f"{base_path}/{name_table}_controller.py"):
            return False

        model_code = f"""
from src.core.config import settings
from src.core.enums.layer import LAYER
from src.core.models.config import Config
from src.core.models.filter import Pagination
from src.core.models.response import Response
from src.core.classes.async_message import Message
from src.core.models.message import MessageCoreEntity
from src.core.enums.keys_message import KEYS_MESSAGES
from src.core.wrappers.execute_transaction import execute_transaction
from src.domain.models.entities.{name_table}.index import (
    {pascal_name_table}Delete,
    {pascal_name_table}Read,
    {pascal_name_table}Save,
    {pascal_name_table}Update,
)
from src.domain.services.use_cases.entities.{name_table}.index import (
    {pascal_name_table}DeleteUseCase,
    {pascal_name_table}ListUseCase,
    {pascal_name_table}ReadUseCase,
    {pascal_name_table}SaveUseCase,
    {pascal_name_table}UpdateUseCase,
)
from src.infrastructure.database.repositories.entities.{name_table}_repository import (
    {pascal_name_table}Repository,
)



{name_table}_repository = {pascal_name_table}Repository()


class {pascal_name_table}Controller:
    def __init__(self) -> None:
        self.{name_table}_save_use_case = {pascal_name_table}SaveUseCase({name_table}_repository)
        self.{name_table}_update_use_case = {pascal_name_table}UpdateUseCase({name_table}_repository)
        self.{name_table}_list_use_case = {pascal_name_table}ListUseCase({name_table}_repository)
        self.{name_table}_delete_use_case = {pascal_name_table}DeleteUseCase({name_table}_repository)
        self.{name_table}_read_use_case = {pascal_name_table}ReadUseCase({name_table}_repository)
        self.message = Message()

    @execute_transaction(layer=LAYER.I_W_C_E.value, enabled=settings.has_track)
    async def save(self, config: Config, params: {pascal_name_table}Save) -> Response:
        result_save = await self.{name_table}_save_use_case.execute(config=config, params=params)
        if isinstance(result_save, str):
            return Response.error(None, result_save)
        return Response.success_temporary_message(
            response=result_save,
            message= await self.message.get_message(
                config=config,
                message=MessageCoreEntity(
                    key=KEYS_MESSAGES.CORE_SAVED_INFORMATION.value
                ),
            ),
        )

    @execute_transaction(layer=LAYER.I_W_C_E.value, enabled=settings.has_track)
    async def update(self, config: Config, params: {pascal_name_table}Update) -> Response:
        result_update = await self.{name_table}_update_use_case.execute(config=config, params=params)
        if isinstance(result_update, str):
            return Response.error(None, result_update)
        return Response.success_temporary_message(
            response=result_update,
            message= await self.message.get_message(
                config=config,
                message=MessageCoreEntity(
                    key=KEYS_MESSAGES.CORE_UPDATED_INFORMATION.value
                ),
            ),
        )

    @execute_transaction(layer=LAYER.I_W_C_E.value, enabled=settings.has_track)
    async def list(self, config: Config, params: Pagination) -> Response:
        result_list = await self.{name_table}_list_use_case.execute(config=config, params=params)
        if isinstance(result_list, str):
            return Response.error(None, result_list)
        return Response.success_temporary_message(
            response=result_list,
            message= await self.message.get_message(
                config=config,
                message=MessageCoreEntity(key=KEYS_MESSAGES.CORE_QUERY_MADE.value),
            ),
        )

    @execute_transaction(layer=LAYER.I_W_C_E.value, enabled=settings.has_track)
    async def delete(self, config: Config, params: {pascal_name_table}Delete) -> Response:
        result_delete = await self.{name_table}_delete_use_case.execute(config=config, params=params)
        if isinstance(result_delete, str):
            return Response.error(None, result_delete)
        return Response.success_temporary_message(
            response=result_delete,
            message= await self.message.get_message(
                config=config,
                message=MessageCoreEntity(
                    key=KEYS_MESSAGES.CORE_DELETION_PERFORMED.value
                ),
            ),
        )

    @execute_transaction(layer=LAYER.I_W_C_E.value, enabled=settings.has_track)
    async def read(self, config: Config, params: {pascal_name_table}Read) -> Response:
        result_delete = await self.{name_table}_read_use_case.execute(config=config, params=params)
        if isinstance(result_delete, str):
            return Response.error(None, result_delete)
        return Response.success_temporary_message(
            response=result_delete,
            message= await self.message.get_message(
                config=config,
                message=MessageCoreEntity(key=KEYS_MESSAGES.CORE_QUERY_MADE.value),
            ),
        )
        """

        file_contents: dict[str, str] = {f"{name_table}_controller.py": model_code}

        for file_name, content in file_contents.items():
            file_path = os.path.join(base_path, file_name)
            self.file_manager.create_file(file_path=file_path, content=content)

        return True

    def infrastructure_web_entities_routes(self, name_table: str):
        pascal_name_table = snake_to_pascal(snake_str=name_table)
        text_id = '"/{id}"'
        base_path = os.path.join(
            self.current_directory, "src", "infrastructure", "web", "entities_routes"
        )
        if not self.file_exists(file_path=f"{base_path}/{name_table}_router.py"):
            return False

        model_code = f"""
from pydantic import UUID4
from src.core.config import settings
from src.core.models.config import Config
from src.core.models.filter import Pagination
from src.core.models.response import Response
from fastapi import APIRouter, Depends, status
from src.core.methods.get_config import get_config
from src.core.enums.permission_type import PERMISSION_TYPE
from src.core.wrappers.check_permissions import check_permissions
from src.core.wrappers.execute_transaction import execute_transaction_route
from src.domain.models.entities.{name_table}.index import (
    {pascal_name_table}Delete,
    {pascal_name_table}Read,
    {pascal_name_table}Save,
    {pascal_name_table}Update,
)
from src.infrastructure.web.controller.entities.{name_table}_controller import (
    {pascal_name_table}Controller,
)


{name_table}_router = APIRouter(
    prefix="/{convert_to_kebab_case(snake_str=name_table)}", tags=["{pascal_name_table}"], responses={{404: {{"description": "Not found"}}}}
)

{name_table}_controller = {pascal_name_table}Controller()


@{name_table}_router.post("", status_code=status.HTTP_200_OK, response_model=Response)
@check_permissions([PERMISSION_TYPE.SAVE.value])
@execute_transaction_route(enabled=settings.has_track)
async def save(params: {pascal_name_table}Save, config: Config = Depends(get_config)) -> Response:
    return await {name_table}_controller.save(config=config, params=params)


@{name_table}_router.put("", status_code=status.HTTP_200_OK, response_model=Response)
@check_permissions([PERMISSION_TYPE.UPDATE.value])
@execute_transaction_route(enabled=settings.has_track)
async def update(
    params: {pascal_name_table}Update, config: Config = Depends(get_config)
) -> Response:
    return await {name_table}_controller.update(config=config, params=params)


@{name_table}_router.post(
    "/list", status_code=status.HTTP_200_OK, response_model=Response
)
@check_permissions([PERMISSION_TYPE.LIST.value])
@execute_transaction_route(enabled=settings.has_track)
async def list(params: Pagination, config: Config = Depends(get_config)) -> Response:
    return await {name_table}_controller.list(config=config, params=params)


@{name_table}_router.delete(
    {text_id}, status_code=status.HTTP_200_OK, response_model=Response
)
@check_permissions([PERMISSION_TYPE.DELETE.value])
@execute_transaction_route(enabled=settings.has_track)
async def delete(id: UUID4, config: Config = Depends(get_config)) -> Response:
    build_params = {pascal_name_table}Delete(id=id)
    return await {name_table}_controller.delete(config=config, params=build_params)


@{name_table}_router.get({text_id}, status_code=status.HTTP_200_OK, response_model=Response)
@check_permissions([PERMISSION_TYPE.READ.value])
@execute_transaction_route(enabled=settings.has_track)
async def read(id: UUID4, config: Config = Depends(get_config)) -> Response:
    build_params = {pascal_name_table}Read(id=id)
    return await {name_table}_controller.read(config=config, params=build_params)

    """

        file_contents: dict[str, str] = {f"{name_table}_router.py": model_code}

        for file_name, content in file_contents.items():
            file_path = os.path.join(base_path, file_name)
            self.file_manager.create_file(file_path=file_path, content=content)

        return True

    def infrastructure_web_routes(self, name_table: str):
        base_path = os.path.join(
            self.current_directory, "src", "infrastructure", "web", "routes"
        )
        filename = f"{base_path}/route.py"

        import_comment = "# imports"
        new_import_line = f"from src.infrastructure.web.entities_routes.{name_table}_router import {name_table}_router"

        include_router_comment = "# include_router"
        new_include_router_line = f"        app.include_router({name_table}_router)"

        self.file_manager.add_line_to_file(
            filename=filename, comment=import_comment, new_line=new_import_line
        )
        self.file_manager.add_line_to_file(
            filename=filename,
            comment=include_router_comment,
            new_line=new_include_router_line,
        )

        return True

    def infrastructure_database_mappers(self, name_table: str):
        pascal_name_table = snake_to_pascal(snake_str=name_table)
        base_path = os.path.join(
            self.current_directory, "src", "infrastructure", "database", "mappers"
        )
        if not self.file_exists(file_path=f"{base_path}/{name_table}_mapper.py"):
            return False

        columns = self.db.inspector.get_columns(name_table)
        pascal_name_table = snake_to_pascal(name_table)
        fields = [col["name"] for col in columns]

        def generate_map_to_entity(pascal_name_table, fields):
            method = f"""
from typing import List
from src.domain.models.entities.{name_table}.index import (
    {pascal_name_table},
    {pascal_name_table}Save,
    {pascal_name_table}Update,
)
from src.infrastructure.database.entities.{name_table}_entity import {pascal_name_table}Entity\n\n
"""
            method += f"def map_to_{name_table}({name_table}_entity: {pascal_name_table}Entity) -> {pascal_name_table}:\n"
            method += f"    return {pascal_name_table}(\n"
            for field in fields:
                method += f"        {field}={name_table}_entity.{field},\n"
            method += f"    )\n\n"
            return method

        def generate_map_to_list_entity(pascal_name_table):
            method = f"def map_to_list_{name_table}({name_table}_entities: List[{pascal_name_table}Entity]) -> List[{pascal_name_table}]:\n"
            method += f"    return [map_to_{name_table}({name_table}) for {name_table} in {name_table}_entities]\n\n"
            return method

        def generate_map_to_entity_entity(pascal_name_table, fields):
            method = f"def map_to_{name_table}_entity({name_table}: {pascal_name_table}) -> {pascal_name_table}Entity:\n"
            method += f"    return {pascal_name_table}Entity(\n"
            for field in fields:
                method += f"        {field}={name_table}.{field},\n"
            method += f"    )\n\n"
            return method

        def generate_map_to_list_entity_entity(pascal_name_table):
            method = f"def map_to_list_{name_table}_entity({name_table}s: List[{pascal_name_table}]) -> List[{pascal_name_table}Entity]:\n"
            method += f"    return [map_to_{name_table}_entity({name_table}) for {name_table} in {name_table}s]\n\n"
            return method

        def generate_map_to_save_entity(pascal_name_table, fields):
            fields = [
                f
                for f in fields
                if f != "id"
                and not f.startswith("created_date")
                and not f.startswith("updated_date")
            ]
            method = f"def map_to_save_{name_table}_entity({name_table}: {pascal_name_table}Save) -> {pascal_name_table}Entity:\n"
            method += f"    return {pascal_name_table}Entity(\n"
            for field in fields:
                method += f"        {field}={name_table}.{field},\n"
            method += f"    )\n\n"
            return method

        def generate_map_to_update_entity(pascal_name_table, fields):
            fields = [
                f
                for f in fields
                if not f.startswith("created_date") and not f.startswith("updated_date")
            ]
            method = f"def map_to_update_{name_table}_entity({name_table}: {pascal_name_table}Update) -> {pascal_name_table}Entity:\n"
            method += f"    return {pascal_name_table}Entity(\n"
            for field in fields:
                method += f"        {field}={name_table}.{field},\n"
            method += f"    )\n\n"
            return method

        methods = ""
        methods += generate_map_to_entity(pascal_name_table, fields)
        methods += generate_map_to_list_entity(pascal_name_table)
        methods += generate_map_to_entity_entity(pascal_name_table, fields)
        methods += generate_map_to_list_entity_entity(pascal_name_table)
        methods += generate_map_to_save_entity(pascal_name_table, fields)
        methods += generate_map_to_update_entity(pascal_name_table, fields)

        file_contents: dict[str, str] = {f"{name_table}_mapper.py": methods}

        for file_name, content in file_contents.items():
            file_path = os.path.join(base_path, file_name)
            self.file_manager.create_file(file_path=file_path, content=content)

        return True

    def infrastructure_database_entities(self, name_table: str):
        pascal_name_table = snake_to_pascal(snake_str=name_table)
        base_path = os.path.join(
            self.current_directory, "src", "infrastructure", "database", "entities"
        )
        if not self.file_exists(file_path=f"{base_path}/{name_table}_entity.py"):
            return False

        columns = self.db.inspector.get_columns(name_table)

        class_code = f"from sqlalchemy.sql import func\n"
        class_code = f"from src.core.config import settings\n"
        class_code += f"from src.core.models.base import Base\n"
        class_code += f"from sqlalchemy import Column, String, Boolean, DateTime, text, Text, Integer, Float, Time\n"
        class_code += f"from sqlalchemy.dialects.postgresql import UUID\n\n"
        class_code += f"class {pascal_name_table}Entity(Base):\n"
        class_code += f"    __tablename__ = '{name_table}'\n"
        class_code += f"    __table_args__ = {{'schema': settings.database_schema}}\n\n"

        for column in columns:
            col_name = column["name"]
            col_type = self.map_column_type(postgres_type=column["type"])
            nullable = column["nullable"]
            default = column["default"]
            primary_key = col_name == "id"
            unique = col_name == "code"
            onupdate = "onupdate=text('now()')" if col_name == "updated_date" else ""

            col_args = [col_type]
            if primary_key:
                col_args.append("primary_key=True")
            if nullable is not None:
                col_args.append(f"nullable={nullable}")
            if default:
                col_args.append(f"server_default=text('{default}')")
            if unique:
                col_args.append("unique=True")
            if onupdate:
                col_args.append(onupdate)

            col_definition = f"    {col_name} = Column({', '.join(col_args)})\n"

            class_code += col_definition

        file_contents: dict[str, str] = {f"{name_table}_entity.py": class_code}

        for file_name, content in file_contents.items():
            file_path = os.path.join(base_path, file_name)
            self.file_manager.create_file(file_path=file_path, content=content)

        return True

    def create_entity_base(self, name_table: str):
        model_code = f"from pydantic import BaseModel, Field, UUID4\n"
        model_code += f"from typing import Optional\n"
        model_code += f"from datetime import datetime\n\n"
        model_code += f"class {snake_to_pascal(snake_str=name_table)}(BaseModel):\n"
        columns = self.db.inspector.get_columns(name_table)
        for column in columns:
            name = column["name"]
            column_type = column["type"]
            nullable = column["nullable"]
            default = column.get("default")

            model_code += f"    {name}: {self.create_fields(column_type=column_type, name=name, nullable=nullable, default=default)}\n"

        model_code += f"\n"
        model_code += "    def dict(self, *args, **kwargs):\n"
        model_code += '        exclude = kwargs.pop("exclude", set())\n'
        model_code += '        exclude.update({"created_date", "updated_date"})\n'
        model_code += (
            "        return super().model_dump(*args, exclude=exclude, **kwargs)\n"
        )

        return model_code

    def create_domain_services_repositories_entities(self, name_table: str):
        pascal_name_table = snake_to_pascal(snake_str=name_table)

        model_code = f"""
from typing import List, Union
from abc import ABC, abstractmethod

from src.core.models.config import Config
from src.core.models.filter import Pagination

from src.domain.models.entities.{name_table}.index import (
    {pascal_name_table},
    {pascal_name_table}Delete,
    {pascal_name_table}Read,
    {pascal_name_table}Update,
)

from src.infrastructure.database.entities.{name_table}_entity import {pascal_name_table}Entity


class I{pascal_name_table}Repository(ABC):
    @abstractmethod
    def save(
        self,
        config: Config,
        params: {pascal_name_table}Entity,
    ) -> Union[{pascal_name_table}, None]:
        pass

    @abstractmethod
    def update(
        self,
        config: Config,
        params: {pascal_name_table}Update,
    ) -> Union[{pascal_name_table}, None]:
        pass

    @abstractmethod
    def list(
        self,
        config: Config,
        params: Pagination,
    ) -> Union[List[{pascal_name_table}], None]:
        pass

    @abstractmethod
    def delete(
        self,
        config: Config,
        params: {pascal_name_table}Delete,
    ) -> Union[{pascal_name_table}, None]:
        pass

    @abstractmethod
    def read(
        self,
        config: Config,
        params: {pascal_name_table}Read,
    ) -> Union[{pascal_name_table}, None]:
        pass
        """

        return model_code

    def create_domain_services_use_cases_entities_delete(self, name_table: str):
        pascal_name_table = snake_to_pascal(snake_str=name_table)

        model_code = f"""
from typing import Union
from src.core.config import settings
from src.core.enums.layer import LAYER
from src.core.models.config import Config
from src.core.classes.async_message import Message
from src.core.models.message import MessageCoreEntity
from src.core.enums.keys_message import KEYS_MESSAGES
from src.core.enums.response_type import RESPONSE_TYPE
from src.core.wrappers.execute_transaction import execute_transaction
from src.domain.models.entities.{name_table}.index import {pascal_name_table}Delete, {pascal_name_table}
from src.domain.services.repositories.entities.i_{name_table}_repository import (
    I{pascal_name_table}Repository,
)


class {pascal_name_table}DeleteUseCase:
    def __init__(self, {name_table}_repository: I{pascal_name_table}Repository):
        self.{name_table}_repository = {name_table}_repository
        self.message = Message()

    @execute_transaction(layer=LAYER.D_S_U_E.value, enabled=settings.has_track)    
    async def execute(
        self,
        config: Config,
        params: {pascal_name_table}Delete,
    ) -> Union[{pascal_name_table}, str, None]:
        result = await self.{name_table}_repository.delete(config=config, params=params)
        if not result:
            return await self.message.get_message(
                config=config,
                message=MessageCoreEntity(
                    key=KEYS_MESSAGES.CORE_RECORD_NOT_FOUND_TO_DELETE.value
                ),
            )

        if config.response_type == RESPONSE_TYPE.OBJECT.value:
            return result
        elif config.response_type == RESPONSE_TYPE.DICT.value:
            return result.dict()

        return result
        """

        return model_code

    def create_domain_services_use_cases_entities_list(self, name_table: str):
        pascal_name_table = snake_to_pascal(snake_str=name_table)

        model_code = f"""
from typing import List, Union
from src.core.config import settings
from src.core.enums.layer import LAYER
from src.core.models.config import Config
from src.core.models.filter import Pagination
from src.core.classes.async_message import Message
from src.core.models.message import MessageCoreEntity
from src.core.enums.keys_message import KEYS_MESSAGES
from src.core.enums.response_type import RESPONSE_TYPE
from src.domain.models.entities.{name_table}.index import {pascal_name_table}
from src.core.wrappers.execute_transaction import execute_transaction
from src.domain.services.repositories.entities.i_{name_table}_repository import (
    I{pascal_name_table}Repository,
)


class {pascal_name_table}ListUseCase:
    def __init__(self, {name_table}_repository: I{pascal_name_table}Repository):
        self.{name_table}_repository = {name_table}_repository
        self.message = Message()

    @execute_transaction(layer=LAYER.D_S_U_E.value, enabled=settings.has_track)
    async def execute(
        self,
        config: Config,
        params: Pagination,
    ) -> Union[List[{pascal_name_table}], str, None]:
        results = await self.{name_table}_repository.list(config=config, params=params)
        if not results:
            return await self.message.get_message(
                config=config,
                message=MessageCoreEntity(
                    key=KEYS_MESSAGES.CORE_NO_RESULTS_FOUND.value
                ),
            )
        if config.response_type == RESPONSE_TYPE.OBJECT.value:
            return results
        elif config.response_type == RESPONSE_TYPE.DICT.value:
            return [result.dict() for result in results]

        return results
        """

        return model_code

    def create_domain_services_use_cases_entities_read(self, name_table: str):
        pascal_name_table = snake_to_pascal(snake_str=name_table)

        model_code = f"""
from typing import Union
from src.core.config import settings
from src.core.enums.layer import LAYER
from src.core.models.config import Config
from src.core.classes.async_message import Message
from src.core.models.message import MessageCoreEntity
from src.core.enums.keys_message import KEYS_MESSAGES
from src.core.enums.response_type import RESPONSE_TYPE
from src.core.wrappers.execute_transaction import execute_transaction
from src.domain.models.entities.{name_table}.index import {pascal_name_table}, {pascal_name_table}Read
from src.domain.services.repositories.entities.i_{name_table}_repository import (
    I{pascal_name_table}Repository,
)


class {pascal_name_table}ReadUseCase:
    def __init__(self, {name_table}_repository: I{pascal_name_table}Repository):
        self.{name_table}_repository = {name_table}_repository
        self.message = Message()

    @execute_transaction(layer=LAYER.D_S_U_E.value, enabled=settings.has_track)
    async def execute(
        self,
        config: Config,
        params: {pascal_name_table}Read,
    ) -> Union[{pascal_name_table}, str, None]:
        result = await self.{name_table}_repository.read(config=config, params=params)
        if not result:
            return await self.message.get_message(
                config=config,
                message=MessageCoreEntity(
                    key=KEYS_MESSAGES.CORE_RECORD_NOT_FOUND.value
                ),
            )

        if config.response_type == RESPONSE_TYPE.OBJECT.value:
            return result
        elif config.response_type == RESPONSE_TYPE.DICT.value:
            return result.dict() 

        return result
        """

        return model_code

    def create_domain_services_use_cases_entities_save(self, name_table: str):
        pascal_name_table = snake_to_pascal(snake_str=name_table)

        model_code = f"""
from typing import Union
from src.core.config import settings
from src.core.enums.layer import LAYER
from src.core.models.config import Config
from src.core.classes.async_message import Message
from src.core.models.message import MessageCoreEntity
from src.core.enums.keys_message import KEYS_MESSAGES
from src.core.enums.response_type import RESPONSE_TYPE
from src.core.wrappers.execute_transaction import execute_transaction
from src.domain.models.entities.{name_table}.index import {pascal_name_table}, {pascal_name_table}Save
from src.domain.services.repositories.entities.i_{name_table}_repository import (
    I{pascal_name_table}Repository,
)
from src.infrastructure.database.mappers.{name_table}_mapper import (
    map_to_save_{name_table}_entity,
)


class {pascal_name_table}SaveUseCase:
    def __init__(self, {name_table}_repository: I{pascal_name_table}Repository):
        self.{name_table}_repository = {name_table}_repository
        self.message = Message()

    @execute_transaction(layer=LAYER.D_S_U_E.value, enabled=settings.has_track)
    async def execute(
        self,
        config: Config,
        params: {pascal_name_table}Save,
    ) -> Union[{pascal_name_table}, str, None]:
        result = map_to_save_{name_table}_entity(params)
        result = await self.{name_table}_repository.save(config=config, params=result)
        if not result:
            return await self.message.get_message(
                config=config,
                message=MessageCoreEntity(
                    key=KEYS_MESSAGES.CORE_ERROR_SAVING_RECORD.value
                ),
            )

        if config.response_type == RESPONSE_TYPE.OBJECT.value:
            return result
        elif config.response_type == RESPONSE_TYPE.DICT.value:
            return result.dict() 

        return result
        """

        return model_code

    def create_domain_services_use_cases_entities_update(self, name_table: str):
        pascal_name_table = snake_to_pascal(snake_str=name_table)

        model_code = f"""
from typing import Union
from src.core.config import settings
from src.core.enums.layer import LAYER
from src.core.models.config import Config
from src.core.classes.async_message import Message
from src.core.models.message import MessageCoreEntity
from src.core.enums.keys_message import KEYS_MESSAGES
from src.core.enums.response_type import RESPONSE_TYPE
from src.core.wrappers.execute_transaction import execute_transaction
from src.domain.models.entities.{name_table}.index import {pascal_name_table}, {pascal_name_table}Update
from src.domain.services.repositories.entities.i_{name_table}_repository import (
    I{pascal_name_table}Repository,
)



class {pascal_name_table}UpdateUseCase:
    def __init__(self, {name_table}_repository: I{pascal_name_table}Repository):
        self.{name_table}_repository = {name_table}_repository
        self.message = Message()

    @execute_transaction(layer=LAYER.D_S_U_E.value, enabled=settings.has_track)
    async def execute(
        self,
        config: Config,
        params: {pascal_name_table}Update,
    ) -> Union[{pascal_name_table}, str, None]:
        result = await self.{name_table}_repository.update(config=config, params=params)
        if not result:
            return await self.message.get_message(
                config=config,
                message=MessageCoreEntity(key=KEYS_MESSAGES.CORE_UPDATE_FAILED.value),
            )

        if config.response_type == RESPONSE_TYPE.OBJECT.value:
            return result
        elif config.response_type == RESPONSE_TYPE.DICT.value:
            return result.dict() 

        return result
        """

        return model_code

    def create_domain_services_use_cases_entities_index(self, name_table: str):
        pascal_name_table = snake_to_pascal(snake_str=name_table)

        model_code = f"""
from .{name_table}_delete_use_case import {pascal_name_table}DeleteUseCase
from .{name_table}_list_use_case import {pascal_name_table}ListUseCase
from .{name_table}_read_use_case import {pascal_name_table}ReadUseCase
from .{name_table}_save_use_case import {pascal_name_table}SaveUseCase
from .{name_table}_update_use_case import {pascal_name_table}UpdateUseCase


__all__ = [
    "{pascal_name_table}DeleteUseCase",
    "{pascal_name_table}ListUseCase",
    "{pascal_name_table}ReadUseCase",
    "{pascal_name_table}SaveUseCase",
    "{pascal_name_table}UpdateUseCase",
]
        """

        return model_code

    def create_entity_save(self, name_table: str):
        model_code = f"from pydantic import BaseModel, Field, UUID4\n"
        model_code += f"from typing import Optional\n"
        model_code += f"from datetime import datetime\n\n"
        model_code += f"class {snake_to_pascal(snake_str=name_table)}Save(BaseModel):\n"
        columns = self.db.inspector.get_columns(name_table)
        for column in columns:
            name = column["name"]
            column_type = column["type"]
            nullable = column["nullable"]
            default = column.get("default")

            exclude_fields = ["id", "created_date", "updated_date"]

            if not name in exclude_fields:
                model_code += f"    {name}: {self.create_fields(column_type=column_type, name=name, nullable=nullable, default=default)}\n"

        return model_code

    def create_entity_update(self, name_table: str):
        model_code = f"from pydantic import BaseModel, Field, UUID4\n"
        model_code += f"from typing import Optional\n"
        model_code += f"from datetime import datetime\n\n"
        model_code += (
            f"class {snake_to_pascal(snake_str=name_table)}Update(BaseModel):\n"
        )
        columns = self.db.inspector.get_columns(name_table)
        for column in columns:
            name = column["name"]
            column_type = column["type"]
            nullable = column["nullable"]
            default = column.get("default")

            exclude_fields = ["created_date", "updated_date"]

            if not name in exclude_fields:
                model_code += f"    {name}: {self.create_fields_update(column_type=column_type, name=name, nullable=nullable, default=default)}\n"

        return model_code

    def create_entity_read(self, name_table: str):
        model_code = (
            f"from pydantic import UUID4, BaseModel, field_validator, Field\n\n"
        )
        model_code += f"class {snake_to_pascal(snake_str=name_table)}Read(BaseModel):\n"
        model_code += f"    id: UUID4 = Field(...)\n"

        return model_code

    def create_entity_delete(self, name_table: str):
        model_code = (
            f"from pydantic import UUID4, BaseModel, field_validator, Field\n\n"
        )
        model_code += (
            f"class {snake_to_pascal(snake_str=name_table)}Delete(BaseModel):\n"
        )
        model_code += f"    id: UUID4 = Field(...)\n"

        return model_code

    def create_fields(self, column_type: Any, name: Any, nullable: Any, default: Any):
        if isinstance(column_type, UUID):
            field_type = "Optional[UUID4]"
            field_default = "Field(default=None)"
        elif isinstance(column_type, VARCHAR):
            field_type = "Optional[str]" if nullable else "str"
            max_length = column_type.length
            if nullable:
                field_default = f"Field(default=None, max_length={max_length})"
            else:
                field_default = f"Field(..., max_length={max_length})"
        elif isinstance(column_type, BOOLEAN):
            field_type = "bool"
            field_default = f"Field(default={default == 'true'})"
        elif isinstance(column_type, TIMESTAMP):
            field_type = "Optional[datetime]"
            field_default = "Field(default_factory=datetime.now)"
        elif isinstance(column_type, INTEGER):
            field_type = "Optional[int]" if nullable else "int"
            if nullable:
                field_default = "Field(default=None)"
            else:
                field_default = (
                    f"Field(default={default})" if default is not None else "Field(...)"
                )
        elif isinstance(column_type, FLOAT):  # Handling Float types
            field_type = "Optional[float]" if nullable else "float"
            if nullable:
                field_default = "Field(default=None)"
            else:
                field_default = (
                    f"Field(default={default})" if default is not None else "Field(...)"
                )
        elif isinstance(column_type, TEXT):
            field_type = "Optional[str]" if nullable else "str"
            if nullable:
                field_default = "Field(default=None)"
            else:
                field_default = (
                    f"Field(default={default})" if default is not None else "Field(...)"
                )
        else:
            field_type = "str"
            field_default = "Field(default=None)"

        return f"{field_type} = {field_default}"

    def create_fields_update(
        self, column_type: Any, name: Any, nullable: Any, default: Any
    ):
        if isinstance(column_type, UUID):
            field_type = "UUID4"
            field_default = "Field(...)"
        elif isinstance(column_type, VARCHAR):
            field_type = "Optional[str]" if nullable else "str"
            max_length = column_type.length
            if nullable:
                field_default = f"Field(default=None, max_length={max_length})"
            else:
                field_default = f"Field(..., max_length={max_length})"
        elif isinstance(column_type, BOOLEAN):
            field_type = "bool"
            field_default = f"Field(default={default == 'true'})"
        elif isinstance(column_type, TIMESTAMP):
            field_type = "Optional[datetime]"
            field_default = "Field(default_factory=datetime.now)"
        elif isinstance(column_type, INTEGER):
            field_type = "Optional[int]" if nullable else "int"
            if nullable:
                field_default = "Field(default=None)"
            else:
                field_default = (
                    f"Field(default={default})" if default is not None else "Field(...)"
                )
        elif isinstance(column_type, FLOAT):  # Handling Float types
            field_type = "Optional[float]" if nullable else "float"
            if nullable:
                field_default = "Field(default=None)"
            else:
                field_default = (
                    f"Field(default={default})" if default is not None else "Field(...)"
                )
        elif isinstance(column_type, TEXT):
            field_type = "Optional[str]" if nullable else "str"
            if nullable:
                field_default = "Field(default=None)"
            else:
                field_default = (
                    f"Field(default={default})" if default is not None else "Field(...)"
                )
        else:
            field_type = "str"
            field_default = "Field(default=None)"

        return f"{field_type} = {field_default}"
