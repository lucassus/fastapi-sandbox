from datetime import date, datetime

from todos.domain.models import Todo
from todos.fake_repository import FakeRepository


def test_hello_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_integration(container, client):
    response = client.get("/todos")

    assert response.status_code == 200
    assert response.json() == []

    response = client.post("/todos", json={"name": "Test todo"})
    assert response.status_code == 200

    response = client.post("/todos", json={"name": "The other todo"})
    assert response.status_code == 200

    response = client.get("/todos")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Test todo", "completed_at": None},
        {"id": 2, "name": "The other todo", "completed_at": None},
    ]

    with container.now.override(lambda: datetime(2021, 1, 8, 11, 22)):
        response = client.put("/todos/1/complete")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Test todo",
        "completed_at": "2021-01-08",
    }


def test_todos_endpoint(container, client):
    # Given
    todos = [
        Todo(id=1, name="Test todo"),
        Todo(id=2, name="The other todo", completed_at=date(2021, 1, 6)),
    ]

    # When
    with container.repository.override(FakeRepository(todos)):
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
    with container.repository.override(FakeRepository(todos)):
        response = client.get("/todos/1")

    # Then
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Test name", "completed_at": None}


def test_todo_endpoint_returns_404(container, client):
    with container.repository.override(FakeRepository([])):
        response = client.get("/todos/1")

    assert response.status_code == 404
