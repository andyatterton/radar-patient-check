from sqlmodel import create_engine, Session
from .config import settings


def get_session():
    db_url = settings.sqlalchemy_database_url
    if not db_url:
        raise ValueError("SQLALCHEMY_DATABASE_URL not set")

    with Session(create_engine(db_url)) as session:
        yield session
