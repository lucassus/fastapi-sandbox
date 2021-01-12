from typing import List

from fastapi import APIRouter, Depends, Path
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from todos.api import schemas
from todos.api.dependencies import get_repository, get_session
from todos.db.repository import Repository
from todos.services import complete_todo, incomplete_todo

router = APIRouter()


@router.get("", response_model=List[schemas.Todo])
def todos_endpoint(
    repository: Repository = Depends(get_repository),
):
    return repository.list()


@router.post("", response_model=schemas.Todo)
def todo_create_endpoint(
    data: schemas.CreateTodo,
    repository: Repository = Depends(get_repository),
    session: Session = Depends(get_session),
):
    todo = repository.create(data.name)
    session.commit()

    return todo


@router.get(
    "/{id}",
    response_model=schemas.Todo,
    responses={404: {"description": "Todo not found"}},
)
def todo_endpoint(
    id: int = Path(..., description="The ID of the todo to get", ge=1),
    repository: Repository = Depends(get_repository),
):
    todo = repository.get(id)

    if todo is None:
        return JSONResponse(status_code=404)

    return todo


# TODO: Handle 404 errors
@router.put("/{id}/complete", response_model=schemas.Todo)
def todo_complete_endpoint(
    id: int,
    repository: Repository = Depends(get_repository),
    session: Session = Depends(get_session),
):
    todo = complete_todo(id, repository=repository)
    session.commit()

    return todo


# TODO: Handle 404 errors
@router.put("/{id}/incomplete", response_model=schemas.Todo)
def todo_incomplete_endpoint(
    id: int,
    repository: Repository = Depends(get_repository),
    session: Session = Depends(get_session),
):
    todo = incomplete_todo(id, repository=repository)
    session.commit()

    return todo
