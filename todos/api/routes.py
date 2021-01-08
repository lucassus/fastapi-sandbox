from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from todos.api import schemas
from todos.container import Container
from todos.db.repositories import AbstractRepository
from todos.domain.services import Service

router = APIRouter()


@router.get("/")
def helo_endpoint():
    return {"message": "Hello World"}


@router.get("/todos", response_model=List[schemas.Todo])
@inject
def todos_endpoint(
    repository: AbstractRepository = Depends(Provide[Container.repository_provider]),
):
    return repository.list()


@router.get(
    "/todos/{id}",
    response_model=schemas.Todo,
    responses={404: {"description": "Todo not found"}},
)
@inject
def todo_endpoint(
    id: int,
    repository: AbstractRepository = Depends(Provide[Container.repository_provider]),
):
    todo = repository.get(id)

    if todo is None:
        return JSONResponse(status_code=404)

    return todo


@router.post("/todos", response_model=schemas.Todo)
@inject
def todo_create_endpoint(
    todo: schemas.CreateTodo,
    repository: AbstractRepository = Depends(Provide[Container.repository_provider]),
):
    return repository.create(todo.name)


@router.put("/todos/{id}/complete", response_model=schemas.Todo)
@inject
def todo_complete_endpoint(
    id: int,
    service: Service = Depends(Provide[Container.service_provider]),
):
    return service.complete(id)


@router.put("/todos/{id}/incomplete", response_model=schemas.Todo)
@inject
def todo_incomplete_endpoint(
    id: int, service: Service = Depends(Provide[Container.service_provider])
):
    return service.incomplete(id)
