from dependency_injector import providers
from fastapi import Depends
from sqlalchemy.orm import Session

from todos.container import Container
from todos.db.session import SessionLocal


def _get_session():
    session = SessionLocal()

    try:
        yield session
    except:
        session.rollback()
    finally:
        session.close()


# TODO: Inline it?
def get_container(session: Session = Depends(_get_session)):
    container = Container(session_provider=providers.Object(session))
    yield container
