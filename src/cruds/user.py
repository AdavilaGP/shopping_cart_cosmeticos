import logging
from fastapi import status, HTTPException
from src.utils import Hash, get_field_or_404
from src.schemas.users import UserSchema
from src.server.database import db
from email_validator import validate_email, EmailNotValidError

logger = logging.getLogger(__name__)

async def create_user(user: UserSchema):
    try:
        # password = Hash.encrypt(user.password)
        # user.password = password

        new_account = True
        try:
            validation = validate_email(user.email, check_deliverability=new_account)
            user.email = validation.email

        except EmailNotValidError as e:
            print(str(e))

        len_password = 3
        if len_password > len(user.password):
            print("Password not valid")

        else:
            user = await db.users_db.insert_one(user.dict()) # insere no db

        if user.inserted_id:
            user = await get_field_or_404(user.inserted_id, db.users_db, 'user')

            return user

    except Exception as e:
        logger.exception(f'create_user.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        

async def get_user(user_id):
    user = await get_field_or_404(user_id, db.users_db, 'user')

    return user