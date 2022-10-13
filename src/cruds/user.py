from fastapi import status, HTTPException
from src.utils import get_field_or_404
from src.schemas.users import UserSchema
from src.server.database import db
from email_validator import validate_email, EmailNotValidError
from bson.objectid import ObjectId


async def create_user(user: UserSchema):
    try:
        new_account = True
        validation = validate_email(user.email, check_deliverability=new_account)
        user.email = validation.email

    except EmailNotValidError as e:
        print(str(e)) 

    user_db = await get_user_by_email(user.email)
    if user_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="message': 'Email already registered")

    len_password = 3
    if len_password > len(user.password):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="message': 'Password not valid")

    user = await db.users_db.insert_one(user.dict()) # insere no db


    if user.inserted_id:
        user = await get_field_or_404(user.inserted_id, db.users_db, 'user')
        return user
        

async def get_user_by_email(user_email):
    try:
        user = await db.users_db.find_one({'email': user_email})
        if user:
            return user

    except Exception as e:
         print(f"get_user.error: {e}")
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


async def delete_user_by_id(user_id):
    user = await db.users_db.find_one({'_id': ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    try:
        await db.users_db.update_one({'_id': ObjectId(user_id)}, {'$set': {'is_active': False}})
        addresses = await db.addresses_db.find_one({'user._id': user['_id']}, {'address': 1})
        if addresses:
            for address in addresses['address']:
                await db.addresses_db.update_many({'address._id': address['_id']}, {'$set': {'address.$.is_active': False}})

        user_orders = await db.orders_db.find({'user_id': user['_id']}).to_list(length=None)
        if user_orders:
            for order in user_orders:
                await db.order_items_db.delete_many({'order_id': ObjectId(order['_id'])})
                await db.orders_db.delete_many({'user_id': ObjectId(user_id)})  

        return {}
    except Exception as e:
        print(f"delete_user_by_id.error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)  
    
    