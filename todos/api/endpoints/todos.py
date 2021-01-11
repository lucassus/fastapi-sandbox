from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from todos.api import schemas
from todos.api.dependencies import get_repository
from todos.db.repository import Repository
from todos.domain.services import complete_todo, incomplete_todo

router = APIRouter()


@router.get("", response_model=List[schemas.Todo])
def todos_endpoint(
    repository: Repository = Depends(get_repository),
):
    return repository.list()


@router.post("", response_model=schemas.Todo)
def todo_create_endpoint(
    todo: schemas.CreateTodo,
    repository: Repository = Depends(get_repository),
):
    return repository.create(todo.name)


@router.get(
    "/{id}",
    response_model=schemas.Todo,
    responses={404: {"description": "Todo not found"}},
)
def todo_endpoint(
    id: int,
    repository: Repository = Depends(get_repository),
):
    todo = repository.get(id)

    if todo is None:
        return JSONResponse(status_code=404)

    return todo


@router.put("/{id}/complete", response_model=schemas.Todo)
def todo_complete_endpoint(
    id: int,
    repository: Repository = Depends(get_repository),
):
    return complete_todo(id, repository=repository)


@router.put("/{id}/incomplete", response_model=schemas.Todo)
def todo_incomplete_endpoint(
    id: int,
    repository: Repository = Depends(get_repository),
):
    return incomplete_todo(id, repository=repository)
