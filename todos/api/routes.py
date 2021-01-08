from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from todos.api import schemas
from todos.api.dependencies import get_container, get_repository
from todos.container import Container
from todos.domain.abstract_repository import AbstractRepository

router = APIRouter()


@router.get("/")
def helo_endpoint():
    return {"message": "Hello World"}


@router.get("/todos", response_model=List[schemas.Todo])
def todos_endpoint(
    repository: AbstractRepository = Depends(get_repository),
):
    return repository.list()


@router.get(
    "/todos/{id}",
    response_model=schemas.Todo,
    responses={404: {"description": "Todo not found"}},
)
def todo_endpoint(
    id: int,
    container: Container = Depends(get_container),
):
    repository = container.repository()
    todo = repository.get(id)

    if todo is None:
        return JSONResponse(status_code=404)

    return todo


@router.post("/todos", response_model=schemas.Todo)
def todo_create_endpoint(
    todo: schemas.CreateTodo,
    repository: AbstractRepository = Depends(get_repository),
):
    return repository.create(todo.name)


@router.put("/todos/{id}/complete", response_model=schemas.Todo)
def todo_complete_endpoint(
    id: int,
    container: Container = Depends(get_container),
):
    service = container.service()
    return service.complete(id)


@router.put("/todos/{id}/incomplete", response_model=schemas.Todo)
def todo_incomplete_endpoint(
    id: int,
    container: Container = Depends(get_container),
):
    service = container.service()
    return service.incomplete(id)
