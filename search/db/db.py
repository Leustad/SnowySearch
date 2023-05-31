import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from search.config import running_config

logging.info(f"<< Config {running_config}")

POSTGRES_DB = running_config.POSTGRES_DB_NAME
POSTGRES_USER = running_config.POSTGRES_USER
POSTGRES_PASSWORD = running_config.POSTGRES_PASS
POSTGRES_HOST = running_config.POSTGRES_HOST
POSTGRES_PORT = running_config.POSTGRES_PORT

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

Base = declarative_base()


def db_session():
    # Database configuration
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    sm = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = sm()
    return session
