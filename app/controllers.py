from typing import Sequence

from advanced_alchemy.filters import CollectionFilter
from litestar import Controller, delete, get, patch, post
from litestar.dto import DTOData
from litestar.exceptions import NotFoundException
from sqlalchemy.exc import NoResultFound

from app.dtos import TodoItemCreateDTO, TodoItemReadDTO, TodoItemUpdateDTO
from app.models import TodoItem
from app.repositories import TodoItemRepository, provide_todoitem_repo


class ItemController(Controller):
    path = "/items"
    dependencies = {"todoitem_repo": provide_todoitem_repo}
    return_dto = TodoItemReadDTO

    @get()
    async def get_items(
        self, todoitem_repo: TodoItemRepository, listo: bool | None = None
    ) -> Sequence[TodoItem]:
        if listo is None:
            return todoitem_repo.list()
        else:
            return todoitem_repo.list(
                CollectionFilter(field_name="listo", values=[listo])
            )

    @get("/{item_id:int}")
    async def get_item(
        self, todoitem_repo: TodoItemRepository, item_id: int
    ) -> TodoItem:
        try:
            return todoitem_repo.get(item_id)
        except NoResultFound as e:
            raise NotFoundException(detail=f"Item {item_id} no encontrado") from e

    @post(dto=TodoItemCreateDTO)
    async def add_item(
        self, todoitem_repo: TodoItemRepository, data: TodoItem
    ) -> TodoItem:
        return todoitem_repo.add(data)

    @patch("/{item_id:int}", dto=TodoItemUpdateDTO)
    async def change_item(
        self, todoitem_repo: TodoItemRepository, item_id: int, data: DTOData[TodoItem]
    ) -> TodoItem:
        try:
            item, _ = todoitem_repo.get_and_update(
                id=item_id, **data.as_builtins(), match_fields=["id"]
            )
            return item
        except NoResultFound as e:
            raise NotFoundException(detail=f"Item {item_id} no encontrado") from e

    @delete("/{item_id:int}")
    async def delete_item(
        self, todoitem_repo: TodoItemRepository, item_id: int
    ) -> None:
        try:
            todoitem_repo.delete(item_id)
        except NoResultFound as e:
            raise NotFoundException(detail=f"Item {item_id} no encontrado") from e
