from fastapi import FastAPI

from todos.adapters.sqlalchemy.session import engine
from todos.adapters.sqlalchemy.tables import create_tables, start_mappers
from todos.entrypoints.api.routes import api_router

create_tables(engine)
start_mappers()


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)

    return app


app = create_app()