from fastapi import APIRouter, status
from src.cruds.product import create_product, get_product_by_id, get_product_by_name, update_product
from src.schemas.products import ProductSchema
from starlette.responses import JSONResponse
from src.utils import parse_json

router = APIRouter(tags=['Products'], prefix='/products')

@router.post("/")
async def create_new_product(product: ProductSchema):
    product = await create_product(product)
    return JSONResponse(content={ 'data': {'product_id': str(product.inserted_id)}},status_code=status.HTTP_200_OK)

@router.get("/{product_id}")
async def get_product_id(product_id: str):
    product = await get_product_by_id(product_id)
    return JSONResponse(content={'data': {'product': product}}, status_code=status.HTTP_200_OK)

@router.get("/name/{product_name}")
async def get_product_name(product_name: str):
    product = await get_product_by_name(product_name)
    return JSONResponse(content={'data': parse_json(product)}, status_code=status.HTTP_200_OK)

# @router.put("/{product_id}")
# async def update_product_id(product_data, product_id: str):
#     data = await update_product(product_data, product_id)
#     return JSONResponse(content={'data': data}, status_code=status.HTTP_200_OK)