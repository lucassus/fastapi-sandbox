from dependency_injector import containers, providers
from sqlalchemy.orm import Session

from todos.db.repositories import Repository
from todos.domain.services import Service


class Container(containers.DeclarativeContainer):
    # A placeholder for SqlAlchemy's session
    session_provider = providers.Dependency(instance_of=Session)

    repository_provider = providers.Factory(Repository, session=session_provider)
    service_provider = providers.Factory(Service, repository=repository_provider)
