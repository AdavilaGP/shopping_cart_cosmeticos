from pydantic import BaseModel, Field

class AddressSchema(BaseModel):
    street: str
    cep: str
    district: str
    city: str
    state: str
    is_delivery: bool = Field(default=True)
    is_active: bool = Field(default=True)
