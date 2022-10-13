from pydantic import BaseModel, Field

class ProductSchema(BaseModel):
    name: str = Field(unique=True) #O unique está permitindo o cadastro de campos com o mesmo valor
    brand: str
    category: str
    description: str
    price: float = Field(gt=0.01)
    inventory: int = Field(gt=0)
