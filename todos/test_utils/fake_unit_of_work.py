from typing import List

from todos.domain.entities import Project
from todos.service_layer.ports import AbstractUnitOfWork
from todos.test_utils.fake_repository import FakeRepository


class FakeUnitOfWork(AbstractUnitOfWork):
    repository: FakeRepository
    committed = False

    def __init__(self, projects: List[Project]):
        self.repository = FakeRepository(projects=projects)

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
