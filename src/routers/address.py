from fastapi import APIRouter, status
from starlette.responses import JSONResponse
from src.cruds.address import create_address, get_addresses, find_address_by_id
from src.schemas.address import Address
from src.utils import parse_json

router = APIRouter(tags=["Address"], prefix="/user/{user_id}/address")


@router.post("/")
async def create_new_address(address: Address, user_id: str):
    address = await create_address(user_id, address)
    return JSONResponse(content={'data': address}, status_code=status.HTTP_200_OK)


@router.get("/")
async def get_address(user_id: str):
    address_list = await get_addresses(user_id)
    return JSONResponse(content={'data': {'user_address': parse_json(address_list)}}, status_code=status.HTTP_200_OK)


@router.get("/{address_id}")
async def get_address_by_id(user_id: str, address_id: str):
    address = await find_address_by_id(user_id, address_id)
    return JSONResponse(content={'data': {'address': parse_json(address)}}, status_code=status.HTTP_200_OK)
