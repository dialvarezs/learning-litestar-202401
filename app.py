from dataclasses import dataclass
from litestar import Litestar, delete, get, patch, post, put
from litestar.exceptions import NotFoundException


@dataclass
class TodoItem:
    id: int
    titulo: str
    listo: bool


@dataclass
class TodoItemUpdate:
    titulo: str | None = None
    listo: bool | None = None


TODO_LIST: list[TodoItem] = [
    TodoItem(id=1, titulo="Comprar pan", listo=False),
    TodoItem(id=2, titulo="Hacer las tareas", listo=True),
    TodoItem(id=3, titulo="Comprar agua", listo=False),
]


def find_item(item_id: int) -> TodoItem:
    for item in TODO_LIST:
        if item.id == item_id:
            return item
    else:
        raise NotFoundException(detail=f"Item {item_id} no encontrado")


@get("/items")
async def get_list(listo: bool | None = None) -> list[TodoItem]:
    if listo is None:
        return TODO_LIST
    return [x for x in TODO_LIST if x.listo == listo]


@get("/items/{item_id:int}")
async def get_item(item_id: int) -> TodoItem:
    return find_item(item_id)


@post("/items")
async def add_item(data: TodoItem) -> list[TodoItem]:
    TODO_LIST.append(data)
    return TODO_LIST


@put("/items/{item_id:int}")
async def update_item(item_id: int, data: TodoItem) -> list[TodoItem]:
    for item in TODO_LIST:
        if item.id == item_id:
            item.id = data.id
            item.titulo = data.titulo
            item.listo = data.listo

            return TODO_LIST
    else:
        raise NotFoundException(detail=f"Item {item_id} no encontrado")


@patch("/items/{item_id:int}")
async def change_item(item_id: int, data: TodoItemUpdate) -> list[TodoItem]:
    item = find_item(item_id)
    if data.titulo is not None:
        item.titulo = data.titulo
    if data.listo is not None:
        item.listo = data.listo

    return TODO_LIST


@delete("/items/{item_id:int}")
async def delete_item(item_id: int) -> None:
    for item in TODO_LIST:
        if item.id == item_id:
            TODO_LIST.remove(item)
            return
    else:
        raise NotFoundException(detail=f"Item {item_id} no encontrado")


app = Litestar([get_list, get_item, add_item, update_item, change_item, delete_item])
