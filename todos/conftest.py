import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, clear_mappers

from todos.api import api_router
from todos.api.dependencies import get_session
from todos.db.tables import metadata, start_mappers


@pytest.fixture(scope="session")
def engine() -> Engine:
    return create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )


@pytest.fixture(scope="session")
def tables(engine):
    metadata.create_all(bind=engine)
    start_mappers()

    yield

    clear_mappers()


@pytest.fixture
def session(engine, tables):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""

    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(session):
    def override_get_session():
        return session

    app = FastAPI()
    app.include_router(api_router)
    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as client:
        yield client
