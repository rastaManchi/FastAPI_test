from typing import List, Optional

from fastapi import APIRouter, HTTPException, Path, Query, status

from ..models import ItemCreate, ItemInDB, ItemUpdate
from ..storage import storage

router = APIRouter()


@router.get(
    "/",
    response_model=List[ItemInDB],
    summary="Получить список элементов",
    response_description="Список элементов, удовлетворяющих условиям фильтрации",
)
def list_items(
    skip: int = Query(
        0,
        ge=0,
        description="Количество элементов, которое нужно пропустить (для пагинации)",
        example=0,
    ),
    limit: int = Query(
        100,
        gt=0,
        le=1000,
        description="Максимальное количество элементов, которое нужно вернуть",
        example=10,
    ),
    name_contains: Optional[str] = Query(
        None,
        description="Фильтр по подстроке в названии элемента",
        example="sample",
    ),
    is_active: Optional[bool] = Query(
        None,
        description="Фильтр по признаку активности элемента",
        example=True,
    ),
):
    return storage.list(
        skip=skip,
        limit=limit,
        name_contains=name_contains,
        is_active=is_active,
    )


@router.get(
    "/{item_id}",
    response_model=ItemInDB,
    summary="Получить элемент по ID",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Элемент с указанным ID не найден"
        }
    },
)
def get_item(
    item_id: int = Path(..., ge=1, description="ID элемента, который нужно получить"),
):
    item = storage.get(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return item


@router.post(
    "/",
    response_model=ItemInDB,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый элемент",
)
def create_item(item_in: ItemCreate):
    return storage.create(item_in)


@router.put(
    "/{item_id}",
    response_model=ItemInDB,
    summary="Обновить существующий элемент (полное/частичное обновление)",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Элемент с указанным ID не найден"
        }
    },
)
def update_item(
    item_id: int = Path(..., ge=1, description="ID элемента, который нужно обновить"),
    item_in: ItemUpdate = ...,
):
    item = storage.update(item_id, item_in)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return item


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить элемент",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Элемент с указанным ID не найден"
        },
        status.HTTP_204_NO_CONTENT: {
            "description": "Элемент успешно удалён, тело ответа пустое"
        },
    },
)
def delete_item(
    item_id: int = Path(..., ge=1, description="ID элемента, который нужно удалить"),
):
    deleted = storage.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )




