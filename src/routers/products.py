from fastapi import APIRouter, status
from src.cruds.product import create_product
from src.schemas.products import ProductSchema
from starlette.responses import JSONResponse

router = APIRouter(tags=['Products'], prefix='/products')

@router.post("/")
async def create_new_product(product: ProductSchema):
    product = await create_product(product)
    return JSONResponse(content={ 'data': {'product_id': str(product.inserted_id)}},status_code=status.HTTP_200_OK)