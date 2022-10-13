from fastapi import APIRouter, status
from src.cruds.product import create_product, get_product_by_id, get_product_by_name, update_product, delete_product
from src.schemas.products import ProductSchema
from starlette.responses import JSONResponse
from src.utils import parse_json

router = APIRouter(tags=['Products'], prefix='/products')

@router.post("/")
async def create_new_product(product: ProductSchema):
    product = await create_product(product)
    return JSONResponse(content={ 'data': {'product': product}},status_code=status.HTTP_200_OK)

@router.delete("/{id}")
async def delete_product_id(id: str):
    deleted_product = await delete_product(id)
    return JSONResponse(content={ 'data': {'product_id': id}},status_code=status.HTTP_200_OK)

@router.get("/{product_id}")
async def get_product_id(product_id: str):
    product = await get_product_by_id(product_id)
    return JSONResponse(content={'data': {'product': product}}, status_code=status.HTTP_200_OK)

@router.get("/name/{product_name}")
async def get_product_name(product_name: str, skip: int = 0, limit: int = 10):
    product = await get_product_by_name(product_name, skip, limit)
    return JSONResponse(content={'data': parse_json(product)}, status_code=status.HTTP_200_OK)

@router.put("/{product_id}")
async def update_product_by_id(product_data: dict, product_id: str):
    data = await update_product(product_data, product_id)
    return JSONResponse(content={'modified_product': parse_json(data)}, status_code=status.HTTP_200_OK)
