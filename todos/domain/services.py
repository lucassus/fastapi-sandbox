from datetime import date
from typing import Callable

from todos.domain.abstract_repository import AbstractRepository
from todos.domain.errors import TodoNotFoundError
from todos.domain.models import Todo


def complete_todo(
    id: int, now: Callable[..., date], repository: AbstractRepository
) -> Todo:
    todo = repository.get(id)
    if not todo:
        raise TodoNotFoundError

    if todo.is_completed:
        return todo

    return repository.update(todo, completed_at=now())


def incomplete_todo(id: int, repository: AbstractRepository) -> Todo:
    todo = repository.get(id)
    if not todo:
        raise TodoNotFoundError

    if not todo.is_completed:
        return todo

    return repository.update(todo, completed_at=None)
