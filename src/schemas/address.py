from typing import List
from pydantic import BaseModel, Field

class Address(BaseModel):
    street: str
    cep: str
    district: str
    city: str
    state: str
    is_delivery: bool = Field(default=True)
