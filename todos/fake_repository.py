from datetime import date
from typing import List, Optional

from todos.domain.abstract_repository import AbstractRepository
from todos.domain.models import Todo


class FakeRepository(AbstractRepository):
    def __init__(self, todos: List[Todo]):
        self._todos = todos

    def get(self, id: int) -> Optional[Todo]:
        try:
            return next(todo for todo in self._todos if todo.id == id)
        except StopIteration:
            return None

    def create(self, name: str) -> Todo:
        todo = Todo(id=self._next_id, name=name)
        self._todos.append(todo)

        return todo

    def update(self, todo: Todo, completed_at: Optional[date]) -> Todo:
        todo.completed_at = completed_at
        return todo

    def list(self) -> List[Todo]:
        return self._todos

    @property
    def _next_id(self) -> int:
        return (
            max(todo.id for todo in self._todos if todo.id) + 1
            if len(self._todos) > 0
            else 1
        )
