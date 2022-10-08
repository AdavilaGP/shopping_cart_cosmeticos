import logging
from fastapi import status, HTTPException
from src.schemas.address import AddressSchema
from bson.objectid import ObjectId
from src.server.database import db
from src.cruds.user import get_user_by_email

logger = logging.getLogger(__name__)

async def get_address_by_user_email(user_email: str):
    user = await get_user_by_email(user_email)
    if not user:
        raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)
    user_address = await db.addresses_db.find_one({'user.email': user_email})
    if not user_address:
        raise HTTPException(detail='Nenhum endereço encontrado para este usuário', status_code=status.HTTP_404_NOT_FOUND)
    return user_address['address']


async def check_user_address(user_email):
    user = await get_user_by_email(user_email)
    if not user:
        raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)
    user_address = await db.addresses_db.find_one({'user.email': user_email})
    if not user_address:
        raise HTTPException(detail='Nenhum endereço encontrado para este usuário', status_code=status.HTTP_404_NOT_FOUND)
    return user_address


async def create_address(user_email: str, address: AddressSchema):
    user = await get_user_by_email(user_email)
    if not user:
        raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)
    user_address = await db.addresses_db.find_one({'user.email': user_email})
    address = address.dict()
    address['_id'] = ObjectId()
    
    if not user_address:
        user_address = await db.addresses_db.insert_one(
            {
                'user': {
                    '_id': user['_id'],
                    'email': user['email']
                },
                'address': [
                    dict(sorted(address.items()))
                ]
            }
        )
        if user_address.inserted_id:
            return 'Endereço criado'
        
    user_address = await db.addresses_db.update_one(
        {'_id': user_address['_id']},
        {
            '$addToSet': {
                'address': dict(sorted(address.items()))
            }
        }
    )
    if user_address.modified_count:
        return {'Endereços adicionados': user_address.modified_count}
    raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED)    


async def find_address_by_id(user_email: str, address_id: str):
    user_address = await check_user_address(user_email)
    address_list = user_address['address']
    address = [v for v in address_list if v['_id'] == ObjectId(address_id)]
    if not address:
        raise HTTPException(detail='Endereço não encontrado', status_code=status.HTTP_404_NOT_FOUND)
    return address
        
        
async def remove_address_by_id(user_email: str, address_id: str):
    user_address = await check_user_address(user_email)
    address_list = user_address['address']
    address = [v for v in address_list if v['_id'] == ObjectId(address_id)]
    if len(address) < 1:
        raise HTTPException(detail='Endereço não encontrado', status_code=status.HTTP_404_NOT_FOUND)
    updated_address_list = [v for v in address_list if v['_id'] != ObjectId(address_id)]
    updated_address_list = await db.addresses_db.update_one(
        {'_id': user_address['_id']},
        {'$set': {'address': updated_address_list}}
    )
    if updated_address_list.modified_count:
        return {}
    raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED)
    # TODO: alterar pedidos abertos que tenham o endereço removido como endereço de entrega

