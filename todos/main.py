from fastapi import FastAPI

from todos.api import routes
from todos.db.session import engine
from todos.db.tables import metadata, start_mappers

metadata.create_all(bind=engine)
start_mappers()


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(routes.router)

    return app


app = create_app()
