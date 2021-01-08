import abc
from datetime import date
from typing import List, Optional

from todos.domain.models import Todo


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, id: int) -> Optional[Todo]:
        ...

    @abc.abstractmethod
    def list(self) -> List[Todo]:
        ...

    @abc.abstractmethod
    def update(self, todo: Todo, completed_at: Optional[date]) -> Todo:
        ...

    @abc.abstractmethod
    def create(self, name: str) -> Todo:
        ...
