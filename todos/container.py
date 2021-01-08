from dependency_injector import containers, providers

from todos.db.repositories import Repository
from todos.domain.services import Service


class Container(containers.DeclarativeContainer):
    session_provider = providers.ThreadSafeSingleton(lambda: None)

    repository_provider = providers.Factory(Repository, session=session_provider)

    service_provider = providers.Factory(Service, repository=repository_provider)
