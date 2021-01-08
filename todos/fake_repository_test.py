from datetime import date

from todos.domain.models import Todo
from todos.fake_repository import FakeRepository


def test_fake_repository():
    repository = FakeRepository([])

    repository.create("Foo")
    repository.create("Bar")

    assert repository.list() == [Todo(id=1, name="Foo"), Todo(id=2, name="Bar")]
    assert repository.get(1) == Todo(id=1, name="Foo")

    todo = repository.get(2)
    assert todo

    updated_todo = repository.update(todo, completed_at=date(2021, 1, 6))
    assert updated_todo.completed_at is not None

    assert repository.get(123) is None
