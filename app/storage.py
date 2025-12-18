from typing import Dict, List, Optional

from .models import ItemCreate, ItemInDB, ItemUpdate


class InMemoryItemStorage:
    def __init__(self) -> None:
        self._items: Dict[int, ItemInDB] = {}
        self._id_seq: int = 0

    def _next_id(self) -> int:
        self._id_seq += 1
        return self._id_seq

    def list(
        self,
        skip: int = 0,
        limit: int = 100,
        name_contains: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> List[ItemInDB]:
        items = list(self._items.values())

        if name_contains:
            items = [
                item for item in items if name_contains.lower() in item.name.lower()
            ]

        if is_active is not None:
            items = [item for item in items if item.is_active == is_active]

        return items[skip : skip + limit]

    def get(self, item_id: int) -> Optional[ItemInDB]:
        return self._items.get(item_id)

    def create(self, data: ItemCreate) -> ItemInDB:
        item_id = self._next_id()
        item = ItemInDB(id=item_id, **data.dict())
        self._items[item_id] = item
        return item

    def update(self, item_id: int, data: ItemUpdate) -> Optional[ItemInDB]:
        stored = self._items.get(item_id)
        if not stored:
            return None

        updated_data = stored.dict()
        for field, value in data.dict(exclude_unset=True).items():
            updated_data[field] = value

        updated_item = ItemInDB(**updated_data)
        self._items[item_id] = updated_item
        return updated_item

    def delete(self, item_id: int) -> bool:
        if item_id in self._items:
            del self._items[item_id]
            return True
        return False


storage = InMemoryItemStorage()



