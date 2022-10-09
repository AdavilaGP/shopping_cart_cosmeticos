from asyncio.windows_utils import PipeHandle
import logging
from turtle import up
from fastapi import HTTPException, status
from src.schemas.order import OrderSchema, OrderItemSchema
from src.server.database import db
from bson.objectid import ObjectId
from src.cruds.address import get_delivery_address

logger = logging.getLogger(__name__)

    
async def get_order_item_by_id(order_item_id):
    try:
        return await db.order_items_db.find_one({'_id': order_item_id})
    except Exception as e:
        logger.exception(f'get_order_item.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
 
    
async def update_total_order_price(order_id, price):
    return await db.orders_db.update_one(
        {'_id': order_id},
        {'$set': {'price': price}}
    )
    

async def get_order_by_paid_status(user_id, status):
    try:
        pipeline = [
            {'$match': {'user_id': user_id }},
            {'$match': {'paid': status }}
        ]
        return await db.orders_db.aggregate(pipeline).to_list(length=None)
    except Exception as e:
        logger.exception(f'get_opened_order.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


async def get_order_by_id(order_id):
    try: 
        return await db.orders_db.find_one({'_id': order_id})
    except Exception as e:
        logger.exception(f'get_order_by_id.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    

async def create_order_item(order, product_id, product_quantity):
    # TODO checar se já existe esse produto no pedido e se sim aumentar a quantidade e atualizar preço do order_item
    product = await db.products_db.find_one({'_id': ObjectId(product_id)})
    if not product:
        raise HTTPException(detail='Produto não encontrado', status_code=status.HTTP_404_NOT_FOUND)
    updated_price = order['price'] + (product['price'] * product_quantity)
    await update_total_order_price(order['_id'], updated_price)
    order_item = OrderItemSchema(order_id=order['_id'], product={'_id': product_id, 'quantity': product_quantity})
    order_item = await db.order_items_db.insert_one(order_item.dict())
    return await get_order_item_by_id(order_item.inserted_id)

    
async def add_item_to_order(item):
    user = await db.users_db.find_one({'_id': ObjectId(item.user_id)})
    if not user:
        raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)
    
    opened_order = await get_order_by_paid_status(item.user_id, False)
    if opened_order:
        return await create_order_item(opened_order[0], item.product_id, item.product_quantity)
            
    delivery_address = await get_delivery_address(user['email'])
    if not delivery_address:
        raise HTTPException(detail='Não existe endereço de entrega padrão para este usuário', status_code=status.HTTP_404_NOT_FOUND)
    
    new_order = OrderSchema(user_id=user['_id'], price=0, address_id=delivery_address[0]['_id'])
    new_order = await db.orders_db.insert_one(new_order.dict())
    created_order = await get_order_by_id(new_order.inserted_id)
    if created_order:
        return await create_order_item(created_order, item.product_id, item.product_quantity)
    
    