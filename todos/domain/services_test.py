from datetime import date

from todos.domain.models import Todo
from todos.domain.services import Service
from todos.fake_repository import FakeRepository


def test_complete():
    # Given
    todo = Todo(id=1, name="Test todo")
    service = Service(repository=FakeRepository([todo]))

    # When
    completed_todo = service.complete(todo.id)

    # Then
    assert completed_todo == todo
    assert completed_todo.completed_at is not None


def test_incomplete():
    # Given
    todo = Todo(id=1, name="Test todo", completed_at=date(2021, 1, 5))
    service = Service(repository=FakeRepository([todo]))

    # When
    completed_todo = service.incomplete(todo.id)

    # Then
    assert completed_todo == todo
    assert completed_todo.completed_at is None
