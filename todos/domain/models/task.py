from dataclasses import dataclass
from datetime import date, datetime
from typing import Callable, List, Optional


@dataclass
class Task:
    name: str
    id: Optional[int] = None
    completed_at: Optional[date] = None

    @property
    def is_completed(self) -> bool:
        return self.completed_at is not None

    def complete(self, now: Callable[..., date] = datetime.utcnow) -> None:
        if not self.is_completed:
            self.completed_at = now()

    def incomplete(self) -> None:
        if self.is_completed:
            self.completed_at = None


def complete_tasks(
    tasks: List[Task], now: Callable[..., date] = datetime.utcnow
) -> None:
    for task in tasks:
        task.complete(now)