import logging
import pydantic

from bson import ObjectId
from fastapi import status, HTTPException
from src.cruds.order import delete_product_from_opened_orders
from src.schemas.products import ProductSchema
from src.server.database import db
from src.server.validation import validate_object_id
from src.utils import get_field_or_404

logger = logging.getLogger(__name__)

async def create_product(product: ProductSchema):

    #Verifica se produto já existe
    product_db = await get_product_by_name(product.name)
    if product_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="message': 'Product already registered")
    
    try:
        product = await db.products_db.insert_one(product.dict())

    #Verifica ObjectId
        if product.inserted_id:
            product = await get_field_or_404(product.inserted_id, db.products_db, 'product')
            return product
    except Exception as e:
        logger.exception(f'create_product.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


async def delete_product(product_id: str):
    try:
        product = await db.products_db.find_one({'_id': ObjectId(product_id)})
        if product:
            await delete_product_from_opened_orders(product_id)
            await db.products_db.delete_one({'_id': ObjectId(product_id)})
            return product
    except Exception as e:
        logger.exception(f'delete_product.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def get_product_by_id(product_id: str):
    return await get_field_or_404(product_id, db.products_db, 'product')

async def get_product_by_name(product_name: str, skip: int, limit: int):
    try:
        pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str #fix objectId and FastAPI conflict
        cursor = db.products_db.find({'name': {'$regex': product_name}}).skip(int(skip)).limit(int(limit))
        products = await cursor.to_list(length = int(limit))
        if products:
            return products
    except Exception as e:
        logger.exception(f'get_product_by_name.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def update_product(product_data: dict, product_id: str):
    try:
        product = await db.products_db.update_one(
            {'_id': validate_object_id(product_id)},
            {'$set': product_data}
        )

        if product.modified_count:
            return await get_product_by_id(product_id)

    except Exception as e:
        logger.exception(f'update_product.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
