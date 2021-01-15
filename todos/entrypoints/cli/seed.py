from datetime import date

import typer
from tabulate import tabulate

from todos.domain.models import Project, Task
from todos.interfaces.db.session import SessionLocal, engine
from todos.interfaces.db.tables import metadata, start_mappers

start_mappers()
session = SessionLocal()


def main(rebuild_db: bool = True):
    if rebuild_db:
        metadata.drop_all(bind=engine)
        metadata.create_all(bind=engine)

    project = Project(name="Work")
    session.add(project)

    # TODO: Backport it
    session.add_all(
        [
            Task(
                name="Learn Python",
                project=project,
                completed_at=date(2021, 1, 9),
            ),
            Task(
                name="Learn Domain Driven Design",
                project=project,
            ),
            Task(name="Do the shopping"),
            Task(name="Clean the house"),
        ]
    )
    session.commit()

    typer.echo("Seeding tasks completed 🚀\n")

    tasks = session.query(Task).all()
    typer.echo(
        tabulate(
            [
                [
                    task.id,
                    task.name,
                    task.project.name if task.project else None,
                    task.completed_at,
                ]
                for task in tasks
            ],
            headers=["Id", "Name", "Project", "Completed At"],
        ),
    )


if __name__ == "__main__":
    typer.run(main)
