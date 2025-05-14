from pydantic import BaseModel
from datetime import datetime




class ProductBase(BaseModel):
    name: str
    price: float


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


class ClientBase(BaseModel):
    login: str | None = None
    fio: str | None = None
    password: str | None = None


class ClientCreate(ClientBase):
    password: str


class Client(ClientBase):
    id: int

    class Config:
        orm_mode = True


class WarehouseBase(BaseModel):
    product_name: str
    quantity: int


class WarehouseCreate(WarehouseBase):
    pass


class Warehouse(WarehouseBase):
    id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    client_fio: str
    product_name: str
    content: str | None = None
    purchase_price: float
    address: str


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
