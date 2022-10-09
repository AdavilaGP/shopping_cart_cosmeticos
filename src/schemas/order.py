import datetime
from pydantic import BaseModel, Field
from bson.objectid import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
        
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("ObjectId inválido")
        return ObjectId(v)
    
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
        

class AddItemSchema(BaseModel):
    user_id: PyObjectId = Field(default_factory=PyObjectId)
    product_id: PyObjectId = Field(default_factory=PyObjectId)
    product_quantity: int
    
      
class OrderSchema(BaseModel):
    user_id: PyObjectId = Field(default_factory=PyObjectId)
    address_id: PyObjectId = Field(default_factory=PyObjectId)
    price: float
    paid: bool = Field(default=False)
    create: datetime.datetime = Field(default=datetime.datetime.now())

    
class OrderItemSchema(BaseModel):
    order_id: PyObjectId = Field(default_factory=PyObjectId)
    product: dict
    
