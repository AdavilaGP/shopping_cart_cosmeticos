from fastapi import APIRouter, status
from starlette.responses import JSONResponse, Response
from src.cruds.address import create_address, get_address_by_user_email, find_address_by_id, remove_address_by_id
from src.schemas.address import AddressSchema
from src.utils import parse_json

router = APIRouter(tags=["Address"], prefix="/user/{user_email}/address")


@router.post("/")
async def create_new_address(address: AddressSchema, user_email: str):
    address = await create_address(user_email, address)
    return JSONResponse(content={'message': address}, status_code=status.HTTP_201_CREATED)


@router.get("/")
async def get_address_list(user_email: str):
    address_list = await get_address_by_user_email(user_email)
    return JSONResponse(content={'address_list': parse_json(address_list)}, status_code=status.HTTP_200_OK)


@router.get("/{address_id}")
async def get_address_by_id(user_email: str, address_id: str):
    address = await find_address_by_id(user_email, address_id)
    return JSONResponse(content={'address': parse_json(address)}, status_code=status.HTTP_200_OK)


@router.delete("/{address_id}")
async def delete_address_by_id(user_email: str, address_id: str):
    await remove_address_by_id(user_email, address_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
