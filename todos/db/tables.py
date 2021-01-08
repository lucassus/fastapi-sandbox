from sqlalchemy import Column, Date, Integer, MetaData, String, Table
from sqlalchemy.orm import mapper

from todos.domain.models import Todo

metadata = MetaData()

todos = Table(
    "todos",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
    # TODO: Change it to datetime
    Column("completed_at", Date, nullable=True),
)


def start_mappers():
    mapper(Todo, todos)
