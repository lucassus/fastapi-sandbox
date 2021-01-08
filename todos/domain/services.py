from datetime import datetime

from todos.domain.abstract_repository import AbstractRepository
from todos.domain.models import Todo


class Service:
    def __init__(self, repository: AbstractRepository):
        self._repository = repository

    def complete(self, id: int) -> Todo:
        todo = self._repository.get(id)
        assert todo

        if todo.is_completed:
            return todo

        return self._repository.update(todo, completed_at=datetime.now())

    def incomplete(self, id: int) -> Todo:
        todo = self._repository.get(id)
        assert todo

        if not todo.is_completed:
            return todo

        return self._repository.update(todo, completed_at=None)
