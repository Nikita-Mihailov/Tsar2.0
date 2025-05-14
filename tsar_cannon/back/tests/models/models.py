from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    price = Column(Float, nullable=False)

    orders = relationship("Order", back_populates="product")


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    fio = Column(String, unique=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)

    orders = relationship("Order", back_populates="client")


class Warehouse(Base):
    __tablename__ = "warehouse"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, default=0)




class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_fio = Column(String, ForeignKey("clients.fio"), nullable=False)
    product_name = Column(String, ForeignKey("product.name"), nullable=False)
    content = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    purchase_price = Column(Float, nullable=False)
    address = Column(String)

    client = relationship("Client", back_populates="orders")
    product = relationship("Product", back_populates="orders")


