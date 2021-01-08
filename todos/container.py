from datetime import datetime

from dependency_injector import containers, providers
from sqlalchemy.orm import Session

from todos.db.repository import Repository
from todos.domain.services import complete_todo, incomplete_todo


class Container(containers.DeclarativeContainer):
    # A placeholder for SqlAlchemy's session
    session = providers.Dependency(instance_of=Session)
    repository = providers.Factory(Repository, session=session)

    now = providers.Callable(datetime.utcnow)

    complete_todo = providers.Callable(complete_todo, now=now, repository=repository)
    incomplete_todo = providers.Callable(incomplete_todo, repository=repository)
