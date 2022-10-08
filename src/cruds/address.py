from src.schemas.address import AddressSchema
from bson.objectid import ObjectId
from src.server.database import db


user = {
    "_id": ObjectId("632f955d05f8a6b497416823"),
    "email": "vanessa@gmail.com",
    "password": "324akf294f",
    "is_active": True,
    "is_admin": False
}

async def get_addresses(user_id):
    try:
        user_address = await db.addresses_db.find_one({'user._id': ObjectId(user_id)})
        
        if user_address:
            return user_address
    
    except Exception as e:
        print(f'get_address.error: {e}')


async def create_address(user_id: str, address: AddressSchema):
    try:
        user_address = await get_addresses(user_id)
        address = address.dict()
        address["_id"] = ObjectId()
        
        if user_address:
            user_address = await db.addresses_db.update_one(
                {'_id': user_address['_id']},
                {
                    '$addToSet': {
                        'address': address
                    }
                }
            )
            
            if user_address.modified_count:
                return {"Endereços adicionados": user_address.modified_count}
        
        user_address = await db.addresses_db.insert_one(
            {
                'user': user,
                'address': [
                    address
                ]
            }
        )
        return "Endereço criado"

    except Exception as e:
        print(f'create_address.error: {e}')

