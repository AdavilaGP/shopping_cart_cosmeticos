import datetime
from decimal import Decimal
from src.schemas.users import UserSchema
from src.schemas.address import AddressSchema

from pydantic import BaseModel, Field

#Modelo base de um produto no carrinho
class OrderSchema (): 
    user: UserSchema
    price: Decimal = Field(max_digits=10, decimal_places=2)
    paid: bool = Field(default=False)
    create: datetime.datetime = Field(default=datetime.datetime.now())
    address: AddressSchema
   
