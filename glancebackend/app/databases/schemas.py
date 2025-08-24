from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, EmailStr

class ProductBaseDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Название товара")
    quantity: int = Field(0, ge=0, description="Количество на складе")
    description: Optional[str] = Field(None, max_length=500, description="Описание товара")
    price: int = Field(..., ge=0, description="Цена товара")
    media_id: Optional[int] = Field(None, description="ID медиафайла")


class UserBaseDTO(BaseModel):
    login: str = Field(..., min_length=3, max_length=50, description="Логин пользователя")

class CartBaseDTO(BaseModel):
    user_id: int = Field(..., description="ID пользователя")

class CartItemBaseDTO(BaseModel):
    product_id: int = Field(..., description="ID товара")
    quantity: int = Field(1, ge=1, description="Количество товара")

class FavouriteBaseDTO(BaseModel):
    user_id: int = Field(..., description="ID пользователя")
    product_id: int = Field(..., description="ID товара")

class ProductAddDTO(ProductBaseDTO):
    model_config = ConfigDict(from_attributes=True)

class UserAddDTO(UserBaseDTO):
    password: str = Field(..., min_length=6, max_length=255, description="Пароль")
    model_config = ConfigDict(from_attributes=True)

class CartAddDTO(CartBaseDTO):
    model_config = ConfigDict(from_attributes=True)

class CartItemAddDTO(CartItemBaseDTO):
    cart_id: int = Field(..., description="ID корзины")
    model_config = ConfigDict(from_attributes=True)

class FavouriteAddDTO(FavouriteBaseDTO):
    model_config = ConfigDict(from_attributes=True)


class ProductResponseDTO(ProductBaseDTO):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserResponseDTO(UserBaseDTO):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CartResponseDTO(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    total_price: int = Field(0, description="Общая стоимость корзины")
    total_quantity: int = Field(0, description="Общее количество товаров")
    model_config = ConfigDict(from_attributes=True)

class CartItemResponseDTO(CartItemBaseDTO):
    id: int
    cart_id: int
    product_name: str = Field(..., description="Название товара")
    product_price: int = Field(..., description="Цена товара")
    total_price: int = Field(..., description="Общая стоимость позиции")
    model_config = ConfigDict(from_attributes=True)

class FavouriteResponseDTO(FavouriteBaseDTO):
    id: int
    added_at: datetime
    product_name: str = Field(..., description="Название товара")
    product_price: int = Field(..., description="Цена товара")
    model_config = ConfigDict(from_attributes=True)

class ProductUpdateDTO(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    quantity: Optional[int] = Field(None, ge=0)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[int] = Field(None, ge=0)
    media_id: Optional[int] = Field(None)
    model_config = ConfigDict(from_attributes=True)

class UserUpdateDTO(BaseModel):
    login: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = Field(None)
    password: Optional[str] = Field(None, min_length=6, max_length=255)
    model_config = ConfigDict(from_attributes=True)

class UserLoginDTO(BaseModel):
    login: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=255)

class UserWithCartDTO(UserResponseDTO):
    cart: Optional[CartResponseDTO] = None
    model_config = ConfigDict(from_attributes=True)

class CartWithItemsDTO(CartResponseDTO):
    items: List[CartItemResponseDTO] = []
    model_config = ConfigDict(from_attributes=True)

class ProductWithDetailsDTO(ProductResponseDTO):
    in_cart: bool = Field(False, description="В корзине пользователя")
    in_favourites: bool = Field(False, description="В избранном пользователя")
    model_config = ConfigDict(from_attributes=True)