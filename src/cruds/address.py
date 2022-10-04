from src.schemas.address import Address
from bson.objectid import ObjectId
from src.server.database import db, connect_db


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
            return parse_json(user_address)
    
    except Exception as e:
        print(f'get_address.error: {e}')


async def create_address(user_id: str, address: Address):
    try:
        await connect_db()
        user_address = await get_addresses(user_id)
        
        if user_address:
            user_address = await db.addresses_db.update_one(
                {'_id': user_address['_id']},
                {
                    '$addToSet': {
                        'address': address.dict()
                    }
                }
            )
            
            return user_address
        
        user_address = await db.addresses_db.insert_one(
            {
                'user': user,
                'address': [
                    address.dict()
                ]
            }
        )
    
        return user_address

    except Exception as e:
        print(f'create_address.error: {e}')

