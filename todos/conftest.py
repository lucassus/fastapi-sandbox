import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, clear_mappers

from todos.api import routes
from todos.api.dependencies import get_container
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
def container(session):
    yield from get_container(session)


@pytest.fixture
def client(container):
    app = FastAPI()
    app.dependency_overrides[get_container] = lambda: container
    app.include_router(routes.router)

    with TestClient(app) as client:
        yield client
