from dependency_injector import containers, providers

from todos.db.repositories import Repository
from todos.db.session import SessionLocal
from todos.domain.services import Service


def get_session():
    session = SessionLocal()

    yield session
    session.close()


class Container(containers.DeclarativeContainer):
    session_provider = providers.Resource(get_session)

    repository_provider = providers.Factory(Repository, session=session_provider)

    service_provider = providers.Factory(Service, repository=repository_provider)
