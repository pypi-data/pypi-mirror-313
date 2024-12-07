from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from mjolnir_arq.core.models.login_db import LoginDB
from sqlalchemy.exc import SQLAlchemyError


class ConnectionPostgresql:
    def __init__(self, loginDB: LoginDB) -> None:
        self.DATABASE_URL = f"postgresql+psycopg2://{loginDB.name_user}:{loginDB.password}@{loginDB.host}:{loginDB.port}/{loginDB.name_db}"
        self.engine = None
        self.session = None
        self.inspector = None
        self.loginDB = loginDB
        self._connect()

    def _connect(self):
        try:
            self.engine = create_engine(
                self.DATABASE_URL,
                pool_size=20,
                connect_args={"options": f"-c search_path={self.loginDB.scheme}"},
            )
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            self.inspector = inspect(self.engine)
            print("SUCESS: Conexión a la base de datos establecida con éxito.")
        except SQLAlchemyError as e:
            print(f"ERROR: Error al conectar con la base de datos: {e}")
            self._disconnect()

    def _disconnect(self):
        if self.session:
            self.session.close()
        if self.engine:
            self.engine.dispose()
        print("INFO: Conexión cerrada.")

    def close(self):
        self._disconnect()

    def get_schemas(self):
        """Obtiene una lista de todos los esquemas disponibles en la base de datos."""
        try:
            return self.inspector.get_schema_names()
        except SQLAlchemyError as e:
            print(f"ERROR: Error al obtener los esquemas: {e}")
            return []

    def get_tables_in_schema(self, schema_name: str):
        """Obtiene una lista de todas las tablas en un esquema específico."""
        try:
            return self.inspector.get_table_names(schema=schema_name)
        except SQLAlchemyError as e:
            print(f"ERROR: Error al obtener tablas del esquema '{schema_name}': {e}")
            return []

    def find_table(self, table_name: str):
        """
        Busca una tabla específica en todos los esquemas y retorna su ubicación.
        Retorna None si no encuentra la tabla.
        """
        try:
            schemas = self.get_schemas()
            for schema in schemas:
                tables = self.get_tables_in_schema(schema)
                if table_name in tables:
                    return {"schema": schema, "table": table_name}
            return None
        except SQLAlchemyError as e:
            print(f"ERROR: Error al buscar la tabla '{table_name}': {e}")
            return None

    def get_table(self, schema_name: str, table_name: str):
        """
        Retorna información detallada sobre una tabla específica en un esquema dado.
        """
        try:
            tables = self.get_tables_in_schema(schema_name)
            if table_name in tables:
                return self.inspector.get_columns(table_name, schema=schema_name)
            else:
                print(
                    f"INFO: La tabla '{table_name}' no existe en el esquema '{schema_name}'."
                )
                return None
        except SQLAlchemyError as e:
            print(
                f"ERROR: Error al obtener la información de la tabla '{table_name}': {e}"
            )
            return None
