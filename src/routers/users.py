from fastapi import APIRouter, status
from src.schemas.users import UserSchema
from src.cruds.user import create_user, get_user_by_email, delete_user_by_id
from starlette.responses import JSONResponse
from pydantic.networks import EmailStr

from src.utils import parse_json

router = APIRouter(tags=['Users'], prefix='/users')


@router.post("/")
async def create_new_user(user: UserSchema):
    user = await create_user(user)
    return JSONResponse(content={ 'data': {'user': user}},status_code=status.HTTP_200_OK)


@router.get("/{user_email}")
async def get_user(user_email: EmailStr):
    user_by_email = await get_user_by_email(user_email)
    print(user_by_email)
    return JSONResponse(content={'data': {'user': parse_json(user_by_email)}}, status_code=status.HTTP_200_OK)


@router.delete("/{user_id}")
async def delete_user(user_id: str):
    await delete_user_by_id(user_id)
    return JSONResponse(content={'data': 'User deleted'}, status_code=status.HTTP_200_OK)