
from functools import cache
from typing import Generator
from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine

import logging

from ClassicalLanguageLearner.deployment_info import is_prod, get_env

PGSQL_DEV_URL = f"postgresql+psycopg://postgres:example@pg:5432"

logger = logging.getLogger()

@cache
def get_engine() -> Engine:
    if not is_prod():
        logger.info("Creating dev db engine.")
        return create_engine(PGSQL_DEV_URL)
    else:
        raise ValueError(f"Failed to create database engine for environment: {get_env()}")
    

def create_db_and_tables():
    SQLModel.metadata.create_all(bind=get_engine())


def get_session() -> Generator[Session]:
    with Session(get_engine()) as session:
        yield session
