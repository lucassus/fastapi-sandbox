from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional

from todos.domain import ensure
from todos.domain.entities.task import Task
from todos.domain.errors import TaskNotFoundError


@dataclass
class Project:
    id: int = field(init=False)
    name: str
    max_unfinished_tasks_number: Optional[int] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, *, name: str) -> Task:
        ensure.max_unfinished_tasks_number_is_not_reached(self)

        task = Task(name=name)
        self.tasks.append(task)

        return task

    def complete_task(self, id: int, now: date) -> Task:
        task = self.get_task(id)
        task.complete(now)

        return task

    def incomplete_task(self, id: int) -> Task:
        task = self.get_task(id)
        task.incomplete()

        ensure.max_unfinished_tasks_number_is_not_reached(self)

        return task

    def get_task(self, id: int) -> Task:
        try:
            # TODO: Add python cheat sheet with list, filters, maps etc
            return next(iter(filter(lambda t: t.id == id, self.tasks)))
        except StopIteration:
            raise TaskNotFoundError

    def complete_tasks(self, now: date):
        for task in self.tasks:
            task.complete(now)
