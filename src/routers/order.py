from fastapi import APIRouter, status
from starlette.responses import JSONResponse
from src.schemas.order import AddItemSchema
from src.utils import parse_json
from src.cruds.order import add_item_to_order

router = APIRouter(tags=["Orders"], prefix="/orders")

@router.post("/")
async def add_order_item(item: AddItemSchema):
    order_item =  await add_item_to_order(item)
    return JSONResponse(content={'data': parse_json(order_item)}, status_code=status.HTTP_201_CREATED)
