import logging
from fastapi import HTTPException, status
from src.schemas.order import OrderSchema, OrderItemSchema, ProductItemsSchema
from src.cruds.user import get_user
from src.server.database import db
from bson.objectid import ObjectId


logger = logging.getLogger(__name__)
    

mock_address = {
    "_id" : ObjectId("633e5031141185849fdb4129"),
    "cep" : "98435000",
    "city" : "São Paulo",
    "district" : "São Paulo",
    "is_delivery" : True,
    "state" : "São Paulo",
    "street" : "Rua Quarenta e Sete, Numero 3"
}
    
    
async def add_order_item(order, product_id, product_quantity):
    product = await db.products_db.find_one({'_id': ObjectId(product_id)})
    if product:
        product = ProductItemsSchema(
            product_id=product_id, 
            name=product['name'], 
            description=product['description'],
            price=product['price'],
            quantity=product_quantity
        )
        order_item = OrderItemSchema(order=order, product=product)
        add_item = await db.order_items_db.insert_one(order_item.dict())
        return add_item.inserted_id
    # raise HTTPException(detail=f'Produto não encontrado', status_code=status.HTTP_404_NOT_FOUND)


async def get_opened_order_by_user_id(user_id):
    # TODO checar se o pedido está pago ou não
    user_order = await db.orders_db.find_one({'user._id': ObjectId(user_id)})
    if user_order:
        return user_order
    # raise HTTPException(detail=f'Pedido aberto não encontrado', status_code=status.HTTP_404_NOT_FOUND)


async def get_order_items(order_id):
    order_items = db.orders_db.find_many({'order._id': order_id})
    return order_items


async def get_order_by_id(order_id):
    return await db.orders_db.find_one({'_id': order_id})

    
async def add_item_to_order(item):
    try:
        user = await db.users_db.find_one({'_id': ObjectId(item.user_id)})
        if user:
            user_order = await get_opened_order_by_user_id(item.user_id)
            if user_order:
                order_item = await add_order_item(user_order, item.product_id, item.product_quantity)
                if order_item:
                    # TODO atualizar preço total do pedido, checar se já existe esse produto no pedido e se sim aumentar a quantidade
                    return order_item
                raise HTTPException(detail=f'Não foi possível adicionar um item ao pedido', status_code=status.HTTP_400_BAD_REQUEST)
            # TODO método que busca o endereço com is_delivery = true
            delivery_address = mock_address
            if delivery_address:
                # TODO calcular preço do pedido
                new_order = OrderSchema(user=user, price=0, address=delivery_address)
                new_order = await db.orders_db.insert_one(new_order.dict())
                created_order = await get_order_by_id(new_order.inserted_id)
                if created_order:
                    order_item = await add_order_item(created_order, item.product_id, item.product_quantity)
                    return {created_order, order_item}
        # raise HTTPException(detail=f'Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.exception(f'add_cart.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    