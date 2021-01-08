from dependency_injector import containers, providers
from sqlalchemy.orm import Session

from todos.db.repository import Repository
from todos.domain.services import Service


class Container(containers.DeclarativeContainer):
    # A placeholder for SqlAlchemy's session
    session = providers.Dependency(instance_of=Session)

    repository = providers.Factory(Repository, session=session)
    service = providers.Factory(Service, repository=repository)
