from datetime import date

from todos.db.repositories import FakeRepository
from todos.domain.models import Todo


def test_hello_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_integration(client):
    response = client.get("/todos")

    assert response.status_code == 200
    assert response.json() == []

    response = client.post("/todos", json={"name": "Test todo"})
    assert response.status_code == 200

    response = client.post("/todos", json={"name": "The other todo"})
    assert response.status_code == 200

    response = client.get("/todos")

    assert response.status_code == 200
    todos = response.json()
    assert len(todos) == 2
    assert todos == [
        {"id": 1, "name": "Test todo", "completed_at": None},
        {"id": 2, "name": "The other todo", "completed_at": None},
    ]


def test_todos_endpoint(container, client):
    # Given
    todos = [
        Todo(id=1, name="Test todo"),
        Todo(id=2, name="The other todo", completed_at=date(2021, 1, 6)),
    ]

    # When
    with container.repository_provider.override(FakeRepository(todos)):
        response = client.get("/todos")

    # Then
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Test todo", "completed_at": None},
        {"id": 2, "name": "The other todo", "completed_at": "2021-01-06"},
    ]


def test_todo_endpoint_returns_todo(container, client):
    # Given
    todos = [Todo(id=1, name="Test name")]

    # When
    with container.repository_provider.override(FakeRepository(todos)):
        response = client.get("/todos/1")

    # Then
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Test name", "completed_at": None}


def test_todo_endpoint_returns_404(container, client):
    with container.repository_provider.override(FakeRepository([])):
        response = client.get("/todos/1")

    assert response.status_code == 404
