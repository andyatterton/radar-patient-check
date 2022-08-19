import os

from dotenv import find_dotenv, load_dotenv
from sqlmodel import Field, SQLModel, create_engine

load_dotenv(find_dotenv())

ukrdc_engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URL"))
key_engine = create_engine(os.getenv("SQLITE_URL"))


class APIKeys(SQLModel, table=True):
    ip: str = Field(primary_key=True)
    key: str


SQLModel.metadata.create_all(key_engine)
