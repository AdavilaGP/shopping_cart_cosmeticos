from pydantic import BaseModel, Field

class ProductSchema(BaseModel):
    name: str = Field(unique=True)
    description: str
    price: float = Field(gt=0.01)
    inventory: int = Field(gt=0)
