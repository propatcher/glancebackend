import datetime
from typing import Optional, List, Annotated
from sqlalchemy import ForeignKey, String, Integer, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class ProductOrm(Base):
    __tablename__ = 'products'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(default=0)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[int] = mapped_column(nullable=False)
    media_id: Mapped[Optional[int]] = mapped_column(nullable=True)
    
    cart_items: Mapped[List["CartItemOrm"]] = relationship(back_populates="product")
    favourites: Mapped[List["FavouriteOrm"]] = relationship(back_populates="product")

class UserOrm(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    
    cart: Mapped["CartOrm"] = relationship(back_populates="user", uselist=False)
    favourites: Mapped[List["FavouriteOrm"]] = relationship(back_populates="user")

class CartOrm(Base):
    __tablename__ = "carts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    
    user: Mapped["UserOrm"] = relationship(back_populates="cart")
    items: Mapped[List["CartItemOrm"]] = relationship(back_populates="cart")
    

class CartItemOrm(Base):
    __tablename__ = "cart_items"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(default=1)
    
    cart: Mapped["CartOrm"] = relationship(back_populates="items")
    product: Mapped["ProductOrm"] = relationship(back_populates="cart_items")
    
class FavouriteOrm(Base):
    __tablename__ = "favourites"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    added_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    user: Mapped["UserOrm"] = relationship(back_populates="favourites")
    product: Mapped["ProductOrm"] = relationship(back_populates="favourites")