from fastapi import APIRouter, status
from starlette.responses import JSONResponse
from src.schemas.order import AddItemSchema
from src.utils import parse_json
from src.cruds.order import add_item_to_order

router = APIRouter(tags=["Orders"], prefix="/orders")

@router.post("/")
async def add_order_item(item: AddItemSchema):
    order = await add_item_to_order(item)
    print(order)
    return JSONResponse(content={'data': {'order': parse_json(order)}}, status_code=status.HTTP_200_OK)
