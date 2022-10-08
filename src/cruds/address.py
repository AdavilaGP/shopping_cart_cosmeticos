import logging
from fastapi import status, HTTPException
from src.schemas.address import Address
from bson.objectid import ObjectId
from src.server.database import db

logger = logging.getLogger(__name__)

# TODO será deletado assim que o método de get user for implementado
user = {
    "_id": ObjectId("632f955d05f8a6b497416823"),
    "email": "vanessa@gmail.com",
    "password": "324akf294f",
    "is_active": True,
    "is_admin": False
}

async def get_addresses(user_id: str):
    address_list = await db.addresses_db.find_one({'user._id': ObjectId(user_id)})
    if not address_list:
        return []
    return address_list


async def create_address(user_id: str, address: Address):
    # TODO verificar se o usuário existe com o método get user by id
    if not user:
        raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)
    user_address = await get_addresses(user_id)
    address = address.dict()
    address['_id'] = ObjectId()
    
    if not user_address:
        user_address = await db.addresses_db.insert_one(
            {
                'user': user,
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
        

async def find_address_by_id(user_id: str, address_id: str):
    # TODO verificar se o usuário existe com o método get user by id
    if not user:
        raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)
    user_address = await get_addresses(user_id)
    if not user_address:
            raise HTTPException(detail='Nenhum endereço encontrado para este usuário', status_code=status.HTTP_404_NOT_FOUND)
    address_list = user_address['address']
    address = [v for v in address_list if v['_id'] == ObjectId(address_id)]
    if not address:
        raise HTTPException(detail='Endereço não encontrado', status_code=status.HTTP_404_NOT_FOUND)
    return address
        
        
async def remove_address_by_id(user_id: str, address_id: str):
    # TODO verificar se o usuário existe com o método get user by id
    if not user:
        raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)
    user_address = await get_addresses(user_id)
    if not user_address:
        raise HTTPException(detail='Nenhum endereço encontrado para este usuário', status_code=status.HTTP_404_NOT_FOUND)
    
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
                
          