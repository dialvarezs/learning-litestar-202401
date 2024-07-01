from dataclasses import dataclass


@dataclass
class TodoItem:
    id: int
    titulo: str
    listo: bool


@dataclass
class TodoItemUpdate:
    titulo: str | None = None
    listo: bool | None = None