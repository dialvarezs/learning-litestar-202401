from litestar import Controller, delete, get, patch, post, put
from litestar.exceptions import NotFoundException
from app.database import TODO_LIST
from app.models import TodoItem, TodoItemUpdate


def find_item(item_id: int) -> TodoItem:
    for item in TODO_LIST:
        if item.id == item_id:
            return item
    else:
        raise NotFoundException(detail=f"Item {item_id} no encontrado")


class ItemController(Controller):
    path = "/items"

    @get()
    async def get_list(self, listo: bool | None = None) -> list[TodoItem]:
        if listo is None:
            return TODO_LIST
        return [x for x in TODO_LIST if x.listo == listo]

    @get("/{item_id:int}")
    async def get_item(self, item_id: int) -> TodoItem:
        return find_item(item_id)

    @post()
    async def add_item(self, data: TodoItem) -> list[TodoItem]:
        TODO_LIST.append(data)
        return TODO_LIST

    @put("/{item_id:int}")
    async def update_item(self, item_id: int, data: TodoItem) -> list[TodoItem]:
        for item in TODO_LIST:
            if item.id == item_id:
                item.id = data.id
                item.titulo = data.titulo
                item.listo = data.listo

                return TODO_LIST
        else:
            raise NotFoundException(detail=f"Item {item_id} no encontrado")

    @patch("/{item_id:int}")
    async def change_item(self, item_id: int, data: TodoItemUpdate) -> list[TodoItem]:
        item = find_item(item_id)
        if data.titulo is not None:
            item.titulo = data.titulo
        if data.listo is not None:
            item.listo = data.listo

        return TODO_LIST

    @delete("/{item_id:int}")
    async def delete_item(self, item_id: int) -> None:
        for item in TODO_LIST:
            if item.id == item_id:
                TODO_LIST.remove(item)
                return
        else:
            raise NotFoundException(detail=f"Item {item_id} no encontrado")
