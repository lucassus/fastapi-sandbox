from datetime import date, datetime

from fastapi import Depends, HTTPException
from starlette import status

from todos.domain.entities import Project
from todos.interfaces.abstract_unit_of_work import AbstractUnitOfWork
from todos.interfaces.db.unit_of_work import UnitOfWork


def get_current_time() -> date:
    return datetime.utcnow()


def get_uow():
    with UnitOfWork() as uow:
        yield uow


def get_project(
    project_id: int,
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> Project:
    project = uow.repository.get(project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unable to find a project with ID={project_id}",
        )

    return project
