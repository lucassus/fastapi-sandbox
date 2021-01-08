from datetime import date

from todos.domain.models import Todo


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


def test_todos_endpoint(session, client):
    # Given
    session.add(Todo(name="Test todo"))
    session.add(Todo(name="The other todo", completed_at=date(2021, 1, 6)))
    session.commit()

    # When
    response = client.get("/todos")

    # Then
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Test todo", "completed_at": None},
        {"id": 2, "name": "The other todo", "completed_at": "2021-01-06"},
    ]


def test_todo_endpoint_returns_todo(session, client):
    session.add(Todo(id=1, name="Test name"))
    response = client.get("/todos/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Test name", "completed_at": None}


def test_todo_endpoint_returns_404(client):
    response = client.get("/todos/1")
    assert response.status_code == 404