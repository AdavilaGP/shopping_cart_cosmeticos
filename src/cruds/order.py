import logging
from fastapi import HTTPException, status
from api.core import settings
from src.schemas.products import ProductSchema
from src.schemas.users import UserSchema
from src.cruds.user import get_user
from src.cruds.product import get_product


logger = logging.getLogger(__name__)

def create_cart(product: ProductSchema, user_id: int):
    try:
        if user_id > 0:
            user_cart: UserSchema = get_user(user_id)
            if not user_cart:
                return f'Usuário não encontrado.'
            else:
                product_cart: ProductSchema = get_product(product._id_product)
                if not product_cart:
                    return f'Produto não encontrado.'
                else:
                    return f'Sucesso'   
                             
                return f'Sucesso.'
        else:
            f'O ID de usuário deve ser maior que 0.'
        
                
        cart_result = 

        return cart_result
    except Exception as e:
        logger.exception(f'add_cart.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def create_new_order()