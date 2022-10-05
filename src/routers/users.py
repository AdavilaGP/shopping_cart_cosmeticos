from fastapi import APIRouter, status
from src.schemas.users import UserSchema
from src.cruds.user import create_user
from starlette.responses import JSONResponse

router = APIRouter(tags=['Users'], prefix='/users')


@router.post("/")
async def create_new_user(user: UserSchema):
    user = await create_user(user)
    return JSONResponse(content={ 'data': {'user': user}},status_code=status.HTTP_200_OK)
