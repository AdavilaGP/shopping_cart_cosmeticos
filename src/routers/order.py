from fastapi import APIRouter, status
from starlette.responses import JSONResponse
#from src.cruds.order import create_address, get_addresses
#from src.schemas.order import Address
from src.utils import parse_json
from src.cruds.order import create_new_order

router = APIRouter(tags=["Orders"], prefix=["/orders"])

@router.post("/{user_id}/{product_id}")
async def create_order(user_id: str, product_id: str):
    order = await create_new_order(user_id,product_id)

