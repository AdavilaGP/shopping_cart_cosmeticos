import logging
from fastapi import HTTPException, status
from src.schemas.order import OrderSchema, OrderItemSchema, ProductItemsSchema
from src.server.database import db
from bson.objectid import ObjectId


logger = logging.getLogger(__name__)
    
# TODO será deletado assim que o método de busca de endereço padrão de entrega for implementado
mock_address = {
    "_id" : ObjectId("633e5031141185849fdb4129"),
    "cep" : "98435000",
    "city" : "São Paulo",
    "district" : "São Paulo",
    "is_delivery" : True,
    "state" : "São Paulo",
    "street" : "Rua Quarenta e Sete, Numero 3"
}
    
async def get_order_item_by_id(order_item_id):
    try:
        return await db.order_items_db.find_one({'_id': order_item_id})
    except Exception as e:
        logger.exception(f'get_order_item.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
 
    
async def create_order_item(order, product_id, product_quantity):
        # TODO atualizar preço total do pedido
        # TODO checar se já existe esse produto no pedido e se sim aumentar a quantidade e atualizar preço do order_item
        product = await db.products_db.find_one({'_id': ObjectId(product_id)})
        if not product:
            raise HTTPException(detail='Produto não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        
        product = ProductItemsSchema(
            product_id=product_id, 
            name=product['name'], 
            description=product['description'],
            price=product['price'],
            quantity=product_quantity
        )
        order_item = OrderItemSchema(order=order, product=product)
        order_item = await db.order_items_db.insert_one(order_item.dict())
        return await get_order_item_by_id(order_item.inserted_id)


async def get_opened_order_by_user_id(user_id):
    # TODO checar se o pedido está aberto ou não (paid=True -> fechado, paid=False -> aberto)
    try:
        return await db.orders_db.find_one({'user._id': ObjectId(user_id)})
    except Exception as e:
        logger.exception(f'get_opened_order_by_user_id.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


async def get_order_by_id(order_id):
    try: 
        return await db.orders_db.find_one({'_id': order_id})
    except Exception as e:
        logger.exception(f'get_order_by_id.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    
async def add_item_to_order(item):
    # TODO substituir por método que busca usuário por id
    user = await db.users_db.find_one({'_id': ObjectId(item.user_id)})
    if not user:
        raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)
    
    opened_order = await get_opened_order_by_user_id(item.user_id)
    if opened_order:
        return await create_order_item(opened_order, item.product_id, item.product_quantity)
            
    # TODO método que busca o endereço com is_delivery = true
    delivery_address = mock_address
    if not delivery_address:
        raise HTTPException(detail='Não existe endereço de entrega padrão para este usuário', status_code=status.HTTP_404_NOT_FOUND)
    
    # TODO calcular preço do pedido
    new_order = OrderSchema(user=user, price=0, address=delivery_address)
    new_order = await db.orders_db.insert_one(new_order.dict())
    created_order = await get_order_by_id(new_order.inserted_id)
    if created_order:
        return await create_order_item(created_order, item.product_id, item.product_quantity)
    
    