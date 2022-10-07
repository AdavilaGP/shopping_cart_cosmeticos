import logging
from bson import ObjectId
from fastapi import status, HTTPException
from src.schemas.products import ProductSchema
from src.server.database import db

logger = logging.getLogger(__name__)

async def create_product(product: ProductSchema):
    try:
        return await db.products_db.insert_one(product.dict())
    except Exception as e:
        logger.exception(f'create_product.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


async def delete_product(product_id: str):
    # TODO: Fazer consulta em todos os carrinhos abertos para poder excluir o produto.
    try:
        product = await db.products_db.find_one({'_id': ObjectId(product_id)})
        if product:
            await db.products_db.delete_one({'_id': ObjectId(product_id)})
            return product
    except Exception as e:
        logger.exception(f'delete_product.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
