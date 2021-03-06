from typing import List

from app.modules.projects.domain.entities import Project
from app.modules.projects.domain.ports import AbstractUnitOfWork
from app.modules.projects.test_utils.fake_repository import FakeRepository


class FakeUnitOfWork(AbstractUnitOfWork):
    repository: FakeRepository
    committed = False

    def __init__(self, projects: List[Project]):
        self.repository = FakeRepository(projects=projects)

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
