from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings

engine = create_engine(settings.database_url, pool_size=20)

session_db = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


