from fastapi import APIRouter, status
from starlette.responses import JSONResponse
from src.schemas.order import ItemSchema
from src.utils import parse_json
from src.cruds.order import (
    add_item_to_order, 
    get_orders_by_user_email,
)

router = APIRouter(tags=["Orders"], prefix="/orders/{user_email}")

@router.post("/")
async def add_order_item(user_email: str, item: ItemSchema):
    order_item =  await add_item_to_order(user_email, item)
    return JSONResponse(content={'order_item': parse_json(order_item)}, status_code=status.HTTP_201_CREATED)


@router.get("/opened")
async def get_opened_order(user_email: str):
    order = await get_orders_by_user_email(user_email, order_status="opened")
    return JSONResponse(content={'order': parse_json(order)}, status_code=status.HTTP_200_OK)


@router.get("/closed")
async def get_closed_orders(user_email: str):
    order = await get_orders_by_user_email(user_email, order_status="closed")
    return JSONResponse(content={'orders': parse_json(order)}, status_code=status.HTTP_200_OK)

