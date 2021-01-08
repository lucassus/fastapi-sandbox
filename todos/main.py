from fastapi import FastAPI, Request

from todos.api import routes
from todos.container import Container
from todos.db.session import SessionLocal, engine
from todos.db.tables import metadata, start_mappers

metadata.create_all(bind=engine)
start_mappers()


def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[routes])

    app = FastAPI()
    app.include_router(routes.router)

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        session = SessionLocal()
        container.session_provider.override(session)

        try:
            response = await call_next(request)
            return response
        finally:
            session.close()
            container.session_provider.reset()

    return app


app = create_app()
