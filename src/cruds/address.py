from fastapi import status, HTTPException
from src.schemas.address import Address
from bson.objectid import ObjectId
from src.server.database import db


user = {
    "_id": ObjectId("632f955d05f8a6b497416823"),
    "email": "vanessa@gmail.com",
    "password": "324akf294f",
    "is_active": True,
    "is_admin": False
}

async def get_addresses(user_id: str):
    try:
        user_address = await db.addresses_db.find_one({'user._id': ObjectId(user_id)})
        
        if user_address:
            return user_address
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Usuário não encontrados')
    
    except Exception as e:
        print(f'get_address.error: {e}')


async def create_address(user_id: str, address: Address):
    try:
        user_address = await get_addresses(user_id)
        address = address.dict()
        address['_id'] = ObjectId()
        
        if user_address:
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

    except Exception as e:
        print(f'create_address.error: {e}')


async def find_address_by_id(user_id: str, address_id: str):
    try:
        user_address = await get_addresses(user_id)
        
        if user_address:
            address_list = user_address['address']
            address = [v for v in address_list if v['_id'] == ObjectId(address_id)]
            if address:
                return address
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Endereço {address_id} não encontrado')
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Usuário ou endereço {address_id} não encontrados')
        
    except Exception as e:
        print(f'get_address_by_id.error: {e}')
        

async def remove_address_by_id(user_id: str, address_id: str):
    try:
        user_address = await get_addresses(user_id)
        
        if user_address:
            address_list = user_address['address']
            updated_address_list = [v for v in address_list if v['_id'] != ObjectId(address_id)]
            address_list = await db.addresses_db.update_one(
                {'_id': user_address['_id']},
                {
                    '$set': {
                        'address': updated_address_list
                    }
                }
            )
            
            if address_list.modified_count:
                return 'Endereço removido'
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Endereço {address_id} não encontrado')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Usuário ou endereço {address_id} não encontrados')
            
    except Exception as e:
        print(f'remove_address_by_id.error: {e}')
        