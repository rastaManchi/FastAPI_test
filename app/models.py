from pydantic import BaseModel, Field
from typing import Optional


class ItemBase(BaseModel):
    name: str = Field(..., description="Название элемента", example="Sample item")
    description: Optional[str] = Field(
        None, description="Описание элемента", example="Какое-то описание"
    )
    price: float = Field(..., gt=0, description="Цена элемента", example=9.99)
    is_active: bool = Field(
        True, description="Флаг активности элемента", example=True
    )


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Название элемента")
    description: Optional[str] = Field(None, description="Описание элемента")
    price: Optional[float] = Field(None, gt=0, description="Цена элемента")
    is_active: Optional[bool] = Field(None, description="Флаг активности элемента")


class ItemInDB(ItemBase):
    id: int = Field(..., description="Уникальный идентификатор элемента", example=1)




