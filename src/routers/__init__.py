from fastapi import APIRouter
from src.routers import users, address, products, order, root

api_router = APIRouter()

api_router.include_router(root.router)
api_router.include_router(users.router)
api_router.include_router(products.router)
api_router.include_router(address.router)
api_router.include_router(order.router)
