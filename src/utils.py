from passlib.context import CryptContext
from fastapi import HTTPException
from src.server.validation import validate_object_id


pwd_encrypted = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def encrypt(self, password):
        return pwd_encrypted.hash(password)

    def verify(self, password, password_encrypted):
        return pwd_encrypted.verify(password, password_encrypted)

async def get_field_or_404(id, collection, field):
    data = await collection.find_one({'_id': validate_object_id(id)})
    if data:
        return fix_id(data)
    raise HTTPException(status_code=404, detail=f'{field} not found')

def fix_id(data):
    if data.get('_id', False):
        data['_id'] = str(data['_id'])
        return data
    raise ValueError(f'_id not found!')