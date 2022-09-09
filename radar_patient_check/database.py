import os

from dotenv import find_dotenv, load_dotenv
from sqlmodel import create_engine

load_dotenv(find_dotenv())

ukrdc_engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URL"))
