from dependency_injector import providers
from dependency_injector.containers import DynamicContainer
from fastapi import Depends
from sqlalchemy.orm import Session

from todos.db.repositories import Repository
from todos.db.session import SessionLocal
from todos.domain.services import Service


def _get_session():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


def get_container(session: Session = Depends(_get_session)):
    container = DynamicContainer()

    container.repository_provider = providers.Factory(Repository, session=session)
    container.service_provider = providers.Factory(
        Service, repository=container.repository_provider
    )

    yield container
