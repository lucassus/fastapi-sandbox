from typing import Callable

from sqlalchemy.orm import Session

from todos.services.project_management.adapters.repository import Repository
from todos.services.project_management.domain.ports import AbstractUnitOfWork


class UnitOfWork(AbstractUnitOfWork):
    repository: Repository

    def __init__(self, session_factory: Callable[..., Session]):
        self._session_factory = session_factory

    def __enter__(self):
        self._session = self._session_factory()
        self.repository = Repository(session=self._session)

        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self._session.close()

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()