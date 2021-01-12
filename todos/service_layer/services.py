from datetime import date, datetime
from typing import Callable

from sqlalchemy.orm import Session

from todos.db.abstract_repository import AbstractRepository
from todos.domain.models.todo import Todo
from todos.service_layer.errors import TodoNotFoundError


def create_todo(name: str, repository: AbstractRepository, session: Session) -> Todo:
    todo = Todo(name=name)

    repository.create(todo)
    session.commit()

    return todo


def complete_todo(
    id: int,
    repository: AbstractRepository,
    session: Session,
    now: Callable[..., date] = datetime.utcnow,
) -> Todo:
    todo = repository.get(id)

    if not todo:
        raise TodoNotFoundError

    todo.complete(now)
    session.commit()

    return todo


def incomplete_todo(
    id: int,
    repository: AbstractRepository,
    session: Session,
) -> Todo:
    todo = repository.get(id)

    if not todo:
        raise TodoNotFoundError

    todo.incomplete()
    session.commit()

    return todo
