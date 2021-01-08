from datetime import date, datetime

from todos.domain.models import Todo
from todos.fake_repository import FakeRepository


def test_complete(container):
    # Given
    todo = Todo(id=1, name="Test todo")
    current_datetime = datetime.now()

    # When
    with container.repository.override(FakeRepository([todo])):
        with container.now.override(lambda: current_datetime):
            completed_todo = container.complete_todo(todo.id)

    # Then
    assert completed_todo == todo
    assert completed_todo.completed_at == current_datetime


def test_incomplete(container):
    # Given
    todo = Todo(id=1, name="Test todo", completed_at=date(2021, 1, 5))

    # When
    with container.repository.override(FakeRepository([todo])):
        completed_todo = container.incomplete_todo(todo.id)

    # Then
    assert completed_todo == todo
    assert completed_todo.completed_at is None
