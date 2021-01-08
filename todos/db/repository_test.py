from datetime import date

from todos.db.repository import Repository
from todos.domain.models import Todo


def test_repository_get(session):
    todo = Todo(name="Test todo")
    session.add(todo)
    session.commit()

    repository = Repository(session=session)
    assert repository.get(1) == todo


def test_repository_get_returns_none(session):
    repository = Repository(session=session)
    assert repository.get(1) is None


def test_repository_list(session):
    repository = Repository(session=session)

    assert repository.list() == []

    todo = Todo(name="One")
    session.add(todo)

    todo = Todo(name="Two")
    session.add(todo)

    session.commit()

    assert len(repository.list()) == 2


def test_repository_update(session):
    repository = Repository(session=session)

    todo = Todo(name="One")
    session.add(todo)
    session.commit()

    repository.update(todo, completed_at=date(2021, 1, 6))
    updated_todo = session.query(Todo).get(todo.id)

    assert updated_todo.completed_at is not None
