from typing import Sequence

from litestar import Controller, delete, get, patch, post
from litestar.dto import DTOData
from litestar.exceptions import NotFoundException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.dtos import TodoItemCreateDTO, TodoItemReadDTO, TodoItemUpdateDTO
from app.models import TodoItem


class ItemController(Controller):
    path = "/items"
    return_dto = TodoItemReadDTO

    @get()
    async def get_items(
        self, db_session: Session, listo: bool | None = None
    ) -> Sequence[TodoItem]:
        stmt = select(TodoItem)
        if listo is not None:
            stmt = stmt.where(TodoItem.listo == listo)

        return db_session.execute(stmt).scalars().all()

    @get("/{item_id:int}")
    async def get_item(self, db_session: Session, item_id: int) -> TodoItem:
        try:
            stmt = select(TodoItem).where(TodoItem.id == item_id)
            return db_session.execute(stmt).scalar_one()
        except NoResultFound:
            raise NotFoundException(detail=f"Item {item_id} no encontrado")

    @post(dto=TodoItemCreateDTO)
    async def add_item(self, db_session: Session, data: TodoItem) -> TodoItem:
        db_session.add(data)
        db_session.commit()

        return data

    @patch("/{item_id:int}", dto=TodoItemUpdateDTO)
    async def change_item(
        self, db_session: Session, item_id: int, data: DTOData[TodoItem]
    ) -> TodoItem:
        try:
            stmt = select(TodoItem).where(TodoItem.id == item_id)
            item = db_session.execute(stmt).scalar_one()

            data.update_instance(item)
            db_session.commit()

            return item
        except NoResultFound:
            raise NotFoundException(detail=f"Item {item_id} no encontrado")

    @delete("/{item_id:int}")
    async def delete_item(self, db_session: Session, item_id: int) -> None:
        try:
            stmt = select(TodoItem).where(TodoItem.id == item_id)
            item = db_session.execute(stmt).scalar_one()
            db_session.delete(item)
            db_session.commit()
        except NoResultFound:
            raise NotFoundException(detail=f"Item {item_id} no encontrado")
