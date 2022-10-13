from fastapi import APIRouter, status
from starlette.responses import JSONResponse, Response
from src.schemas.order import ItemSchema
from src.utils import parse_json
from src.cruds.order import (
    add_item_to_order,
    close_order, 
    get_orders_by_user_email,
    remove_item_from_order,
    remove_order_by_id
)

router = APIRouter(tags=["Orders"], prefix="/orders/{user_email}")

@router.post("/")
async def add_order_item(user_email: str, item: ItemSchema):
    order_item =  await add_item_to_order(user_email, item)
    return JSONResponse(content={'order_item': parse_json(order_item)}, status_code=status.HTTP_201_CREATED)


@router.get("/order/")
async def get_opened_order(user_email: str, order_status: str, orders_quantity: bool = None):
    order = await get_orders_by_user_email(user_email, order_status)
    if not orders_quantity:
        return JSONResponse(content={'order': parse_json(order)}, status_code=status.HTTP_200_OK)
    return JSONResponse(content={'quantidade_pedidos': len(order)}, status_code=status.HTTP_200_OK)
    

@router.delete("/")
async def remove_order_item(user_email: str, item: ItemSchema):
    await remove_item_from_order(user_email, item)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/order/{order_id}")
async def remove_order(user_email: str, order_id: str):
    await remove_order_by_id(user_email, order_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/order/{order_id}")
async def close_opened_order(user_email, order_id):
    order = await close_order(user_email, order_id)
    return JSONResponse(content={'order': parse_json(order)}, status_code=status.HTTP_200_OK)

