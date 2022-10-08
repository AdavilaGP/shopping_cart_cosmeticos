import logging
import pydantic
from bson import ObjectId
from fastapi import status, HTTPException
from src.utils import Hash, get_field_or_404
from src.schemas.products import ProductSchema
from src.server.database import db
from src.server.validation import validate_object_id

logger = logging.getLogger(__name__)

async def create_product(product: ProductSchema):
    try:
        return await db.products_db.insert_one(product.dict())
    except Exception as e:
        logger.exception(f'create_product.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def get_product_by_id(product_id: str):
    return await get_field_or_404(product_id, db.products_db, 'product')

async def get_product_by_name(product_name: str):
    try:
        pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str #fix objectId and FastAPI conflict
        cursor = db.products_db.find({'name': {'$regex': product_name}})
        products = await cursor.to_list(length = 5)
        if products:
            return products
    except Exception as e:
        logger.exception(f'get_product_by_name.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def update_product(product_id: str, product_data):
    try:
        data = {k: v for k, v in product_data.items() if v is not None}
        print(data)

        product = await db.products_db.update_one(
            {'_id': validate_object_id(product_id)},
            {'$set': data}
        )

        if product.modified_count:
            return get_product_by_id(product_id)

    except Exception as e:
        logger.exception(f'update_product.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)