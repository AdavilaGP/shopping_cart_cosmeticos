from asyncio.windows_utils import PipeHandle
import logging
from turtle import up
from fastapi import HTTPException, status
from src.schemas.order import OrderSchema, OrderItemSchema
from src.server.database import db
from bson.objectid import ObjectId
from src.cruds.address import get_delivery_address
from src.cruds.user import get_user_by_email

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
    

async def get_order_by_paid_status(user_id, order_status):
    try:
        order_status = False if order_status == "opened" else True
        return await db.orders_db.find(
            {'$and': [{'user_id': user_id}, {'paid': order_status}]}
        ).to_list(length= None)
        
    except Exception as e:
        logger.exception(f'get_order_by_paid_status.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


async def get_order_by_id(order_id):
    try: 
        return await db.orders_db.find_one({'_id': order_id})
    except Exception as e:
        logger.exception(f'get_order_by_id.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    

async def create_order_item(order, product_id, product_quantity):
    if product_quantity < 1:
        raise HTTPException(detail='Quantidade não pode ser menor que 1', status_code=status.HTTP_400_BAD_REQUEST)
    
    product = await db.products_db.find_one({'_id': ObjectId(product_id)})
    if not product:
        raise HTTPException(detail='Produto não encontrado', status_code=status.HTTP_404_NOT_FOUND)
    
    updated_price = order['price'] + (product['price'] * product_quantity)
    await update_total_order_price(order['_id'], updated_price)
    
    order_item = await db.order_items_db.find_one(
        { '$and': [{'order_id': order['_id']}, {'product._id': product_id}]}
    )
    if order_item:
        updated_quantity = order_item['product']['quantity'] + product_quantity
        updated_order_item = await db.order_items_db.update_one(
            {'_id': order_item['_id']},
            {'$set': {'product.quantity': updated_quantity}}
        )
        if updated_order_item.modified_count:
            return await get_order_item_by_id(order_item['_id'])
    
    order_item = OrderItemSchema(order_id=order['_id'], product={'_id': product_id, 'quantity': product_quantity})
    order_item = await db.order_items_db.insert_one(order_item.dict())
    return await get_order_item_by_id(order_item.inserted_id)

    
async def add_item_to_order(user_email, item):
    user = await get_user_by_email(user_email)
    if not user:
        raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)
    
    opened_order = await get_order_by_paid_status(user['_id'], False)
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


async def get_orders_by_user_email(user_email, order_status):
    user = await get_user_by_email(user_email)
    if not user:
        raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)
    
    orders = await get_order_by_paid_status(user['_id'], order_status)
    if not orders:
        raise HTTPException(detail='Nenhum pedido encontrado', status_code=status.HTTP_404_NOT_FOUND)
    for order in orders:
        order_items = await db.order_items_db.find(
        {'order_id': order['_id']},
        {'product': 1}
        ).to_list(length=None)
        order['items'] = order_items
    return orders


# user 1: 632f955d05f8a6b497416823
# user 2: 633e0891443a2bf22947179d
# product 1: 633f6144da7ebbccd1b22bbe
# product 2: 633f63e1977580b5b3f2b25f


