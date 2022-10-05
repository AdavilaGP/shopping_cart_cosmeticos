from fastapi import APIRouter
from src.routers import users, address

api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(address.router)
