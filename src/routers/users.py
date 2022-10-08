from fastapi import APIRouter, status
from src.schemas.users import UserSchema
from src.cruds.user import create_user, get_user_by_email
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
    print(user_email)
    user_by_email = await get_user_by_email(user_email)
    print(user_by_email)
    return JSONResponse(content={'data': {'user': parse_json(user_by_email)}}, status_code=status.HTTP_200_OK)