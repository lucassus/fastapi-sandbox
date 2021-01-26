from fastapi import APIRouter

from todos.services.accounts.entrypoints.routes import users

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
