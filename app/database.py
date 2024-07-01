from app.models import TodoItem


TODO_LIST: list[TodoItem] = [
    TodoItem(id=1, titulo="Comprar pan", listo=False),
    TodoItem(id=2, titulo="Hacer las tareas", listo=True),
    TodoItem(id=3, titulo="Comprar agua", listo=False),
]

