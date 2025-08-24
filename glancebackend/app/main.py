import asyncio
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
import sys
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from databases.schemas import ProductAddDTO
from databases.database import async_session_factory
from databases.models import ProductOrm

app = FastAPI()

async def get_session():
    async with async_session_factory() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

@app.get("/")
async def test():
    return {"Succes":True}

@app.post("/add_product", tags=["Товары"],summary="Добавить товар")
async def add_product(product_data: ProductAddDTO,session: SessionDep):
    try:
        new_product = ProductOrm(
            name=product_data.name,
            quantity=product_data.quantity,
            description=product_data.description,
            price=product_data.price,
            media_id=product_data.media_id,
        )
        
        session.add(new_product)
        
        await session.commit()
        
        await session.refresh(new_product)
        
        return {
            "message": "Product created successfully",
            "product_id": new_product.id,
            "product_name": new_product.name
        }
        
    except Exception:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating product"
        )
@app.get("/get_products", tags=["Товары"],summary="Получить все товары")
async def get_products(session: SessionDep):
    query = select(ProductOrm)
    result = await session.execute(query)
    products = result.scalars().all()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Products not found"
        )
    return products

@app.get("/products/{product_id}", tags=["Товары"],summary="Получить товар по ID")
async def get_product(product_id: int,session: SessionDep):
    query = select(ProductOrm)
    result = await session.execute(
        select(ProductOrm).where(ProductOrm.id == product_id)
    )
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product_id} not found"
        )
    return product
    
@app.delete("/products/{product_id}", tags=["Товары"],summary="Удалить товар по ID")
async def delete_product(product_id: int, session: SessionDep):
    query = select(ProductOrm)
    result = await session.execute(
    select(ProductOrm).where(ProductOrm.id == product_id))
    products = result.scalar_one_or_none()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    await session.delete(products)
    await session.commit()
    return {"message": "Product deleted successfully"}

@app.put("/products/{product_id}",tags=["Товары"],summary="Обновить товар")
async def update_product(product_id: int,product_data: ProductAddDTO,session: SessionDep):
    try:
        result = await session.execute(
            select(ProductOrm).where(ProductOrm.id == product_id)
        )
        product = result.scalar_one_or_none()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found"
            )
        
        product.name = product_data.name
        product.quantity = product_data.quantity
        product.description = product_data.description
        product.price = product_data.price
        product.media_id = product_data.media_id
        
        await session.commit()
        await session.refresh(product)
        return product
    except Exception:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating products"
        )