import logging
from fastapi import status, HTTPException
from src.utils import Hash, get_field_or_404
from src.schemas.products import ProductSchema
from src.server.database import db

logger = logging.getLogger(__name__)

async def create_product(product: ProductSchema):
    try:
        return await db.products_db.insert_one(product.dict())
    except Exception as e:
        logger.exception(f'create_product.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
