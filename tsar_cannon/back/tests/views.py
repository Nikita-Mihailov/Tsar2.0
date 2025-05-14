import json

from fastapi import APIRouter, HTTPException, Response
from sqlalchemy import select, text
from starlette import status
from starlette.responses import JSONResponse
from .database import get_session
from fastapi_utils.cbv import cbv
from .schemas import ProductBase, ProductCreate, ClientBase, WarehouseBase, OrderBase
from fastapi.encoders import jsonable_encoder
from .models.models import Product, Client, Warehouse, Order

router = APIRouter(prefix="/api")

@cbv(router)
class ProductViewSet:
    model = Product

    @router.post("/product/", tags=["product"])
    async def create_products(
            self,
            new_product: ProductCreate
    ):
        new_object = self.model(**new_product.model_dump(exclude_none=True))
        session = await get_session()
        session.add(new_object)
        await session.commit()
        await session.close()
        return JSONResponse( jsonable_encoder(new_object), status_code=status.HTTP_201_CREATED)

    @router.get("/product/list/", tags=["product"])
    async def products_list(
        self,
        skip: int = 0,
        limit: int = 100,
    ):
        db = await get_session()
        query = select(self.model).offset(skip).limit(limit)
        result = await db.execute(query)
        response_data = result.scalars().all()
        if not response_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Введите корректные skip и limit")
        await db.close()
        return JSONResponse(jsonable_encoder(response_data), status_code=status.HTTP_200_OK)


    @router.get("/product/", tags=["product"])
    async def product_by_name(
        self,
        product_name: str,
    ):
        db = await get_session()
        query = select(self.model).filter(self.model.name == product_name)
        result = await db.execute(query)
        response_data = result.scalars().first()
        if not response_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Продукт с name = {product_name} не найден")
        await db.close()
        return JSONResponse(jsonable_encoder(response_data), status_code=status.HTTP_200_OK)

    @router.patch("/product/", tags=["product"])
    async def products_edit(
        self,
        product_name: str,
        editables: ProductBase
    ):
        db = await get_session()
        query = select(self.model).filter(self.model.name == product_name)
        result = await db.execute(query)
        result = result.scalars().first()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Продукт с name = {product_name} не найден")
        if editables.name:
            result.name = editables.name
        if editables.price:
            result.price = editables.price
        await db.commit()

        await db.close()
        return JSONResponse(jsonable_encoder(result), status_code=status.HTTP_200_OK)

    @router.delete("/product/", tags=["product"])
    async def product_delete(
        self,
        product_name: str,
    ):
        db = await get_session()
        query = select(self.model).filter(self.model.name == product_name)
        result = await db.execute(query)
        result = result.scalars().first()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Продукт с name = {product_name} не найден")
        await db.delete(result)
        await db.commit()
        await db.close()
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@cbv(router)
class ClientViewSet:
    model = Client

    @router.post("/client/", tags=["client"])
    async def create_client(
            self,
            new_client: ClientBase
    ):
        new_client = self.model(**new_client.model_dump(exclude_none=True))
        session = await get_session()
        session.add(new_client)
        await session.commit()
        await session.close()
        return JSONResponse(jsonable_encoder(new_client), status_code=status.HTTP_201_CREATED)

    @router.get("/client/list/", tags=["client"])
    async def client_list(
            self,
            skip: int = 0,
            limit: int = 100,
    ):
        db = await get_session()
        query = text(f"SELECT * FROM clients OFFSET {skip} LIMIT {limit}")
        result = await db.execute(query)
        response_data = result.mappings().all()
        if not response_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Введите корректные skip и limit")
        await db.close()
        return JSONResponse(jsonable_encoder(response_data), status_code=status.HTTP_200_OK)

    @router.get("/client/", tags=["client"])
    async def client_by_name(
        self,
        client_login: str,
    ):
        db = await get_session()
        query = select(self.model).filter(self.model.login == client_login)
        result = await db.execute(query)
        response_data = result.scalars().first()
        if response_data == None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Пользователя с login = {client_login} не найден")
        await db.close()
        return JSONResponse(jsonable_encoder(response_data), status_code=status.HTTP_200_OK)

    @router.patch("/client/", tags=["client"])
    async def client_edit(
        self,
        client_login: str,
        editables: ClientBase
    ):
        db = await get_session()
        query = select(self.model).filter(self.model.login == client_login)
        result = await db.execute(query)
        result = result.scalars().first()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Пользователя с login = {client_login} не найден")
        if editables.fio:
            result.fio = editables.fio
        if editables.login:
            result.login = editables.login
        if editables.password:
            result.password = editables.password
        await db.commit()
        await db.close()
        return JSONResponse(jsonable_encoder(result), status_code=status.HTTP_200_OK)

    @router.delete("/client/", tags=["client"])
    async def client_delete(
        self,
        client_login: str,
    ):
        db = await get_session()
        product = select(self.model).filter(self.model.login == client_login)
        result = await db.execute(product)
        result = result.scalars().first()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Пользователя с login = {client_login} не найден")
        await db.delete(result)
        await db.commit()
        await db.close()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

@cbv(router)
class WarehouseViewSet:
    model = Warehouse

    @router.post("/warehouse/", tags=["warehouse"])
    async def create_warehouse(
            self,
            new_warehouse: WarehouseBase
    ):
        new_client = self.model(**new_warehouse.model_dump(exclude_none=True))
        session = await get_session()
        session.add(new_client)
        await session.commit()
        await session.close()
        return JSONResponse(jsonable_encoder(new_client), status_code=status.HTTP_201_CREATED)

    @router.get("/warehouse/list/", tags=["warehouse"])
    async def warehouse_list(
            self,
            skip: int = 0,
            limit: int = 100,
    ):
        db = await get_session()
        query = select(self.model).offset(skip).limit(limit)
        result = await db.execute(query)
        response_data = result.scalars().all()
        if not response_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Введите корректные skip и limit")
        await db.close()
        return JSONResponse(jsonable_encoder(response_data), status_code=status.HTTP_200_OK)

    @router.get("/warehouse/", tags=["warehouse"])
    async def warehouse_by_name(
            self,
            product_name: str,
    ):
        db = await get_session()
        query = select(self.model).filter(self.model.product_name == product_name)
        result = await db.execute(query)
        response_data = result.scalars().first()
        if response_data == None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Товар с product_id = {product_name} не найден")
        await db.close()
        return JSONResponse(jsonable_encoder(response_data), status_code=status.HTTP_200_OK)

    @router.patch("/warehouse/", tags=["warehouse"])
    async def warehouse_edit(
            self,
            product_name: str,
            editables: WarehouseBase
    ):
        db = await get_session()
        query = select(self.model).filter(self.model.product_name == product_name)
        result = await db.execute(query)
        result = result.scalars().first()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Товар с product_id = {product_name} не найден")
        if editables.product_name:
            result.product_name = editables.product_name
        if editables.quantity:
            result.quantity = editables.quantity
        await db.commit()
        await db.close()
        return JSONResponse(jsonable_encoder(result), status_code=status.HTTP_200_OK)

    @router.delete("/warehouse/", tags=["warehouse"])
    async def warehouse_delete(
            self,
            product_name: str,
    ):
        db = await get_session()
        product = select(self.model).filter(self.model.product_name == product_name)
        result = await db.execute(product)
        result = result.scalars().first()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Товар с product_id = {product_name} не найден")
        await db.delete(result)
        await db.commit()
        await db.close()
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@cbv(router)
class OrderViewSet:
    model = Order

    @router.post("/order/", tags=["order"])
    async def create_order(
            self,
            new_order: OrderBase
    ):
        new_order = self.model(**new_order.model_dump(exclude_none=True))
        session = await get_session()
        session.add(new_order)
        await session.commit()
        await session.close()
        return JSONResponse(jsonable_encoder(new_order), status_code=status.HTTP_201_CREATED)

    @router.get("/order/list/", tags=["order"])
    async def order_list(
            self,
            skip: int = 0,
            limit: int = 100,
    ):
        db = await get_session()
        query = select(self.model).offset(skip).limit(limit)
        result = await db.execute(query)
        response_data = result.scalars().all()
        if not response_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Введите корректные skip и limit")
        await db.close()
        return JSONResponse(jsonable_encoder(response_data), status_code=status.HTTP_200_OK)

    @router.get("/order/", tags=["order"])
    async def order_by_name(
            self,
            product_name: str,
            client_fio: str
    ):
        db = await get_session()
        query = select(self.model).filter(self.model.product_name == product_name, self.model.client_fio == client_fio)
        result = await db.execute(query)
        response_data = result.scalars().first()
        if response_data == None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Транзакция с product_id = {product_name} и client_id = {client_fio} не найдена")
        await db.close()
        return JSONResponse(jsonable_encoder(response_data), status_code=status.HTTP_200_OK)

    @router.patch("/order/", tags=["order"])
    async def order_edit(
            self,
            editables: OrderBase
    ):
        db = await get_session()
        query = select(self.model).filter(self.model.product_id == editables.product_name, self.model.client_fio == editables.client_fio)
        result = await db.execute(query)
        result = result.scalars().first()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Транзакция с product_id = {editables.product_name} и client_id = {editables.client_fio} не найдена")
        if editables.warehouse:
            result.warehouse = editables.warehouse
        if editables.quantity:
            result.quantity = editables.quantity
        await db.commit()
        await db.close()
        return JSONResponse(jsonable_encoder(result), status_code=status.HTTP_200_OK)

    @router.delete("/order/", tags=["order"])
    async def order_delete(
            self,
            product_name: str,
            client_fio: str
    ):
        db = await get_session()
        product = select(self.model).filter(self.model.product_name == product_name, self.model.client_fio ==client_fio)
        result = await db.execute(product)
        result = result.scalars().first()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Транзакция с product_id = {product_name} и client_id = {client_fio} не найдена")
        await db.delete(result)
        await db.commit()
        await db.close()
        return Response(status_code=status.HTTP_204_NO_CONTENT)