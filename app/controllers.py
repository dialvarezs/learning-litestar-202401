from datetime import datetime
from typing import Sequence

from advanced_alchemy.exceptions import NotFoundError
from advanced_alchemy.filters import CollectionFilter
from litestar import Controller, delete, get, patch, post
from litestar.dto import DTOData
from litestar.exceptions import HTTPException, NotFoundException
from sqlalchemy import select
from sqlalchemy.sql.functions import user

from app.dtos import (
    CategoryCreateDTO,
    CategoryReadDTO,
    CategoryReadFullDTO,
    CategoryUpdateDTO,
    TodoItemCreateDTO,
    TodoItemReadDTO,
    TodoItemReadFullDTO,
    TodoItemUpdateDTO,
    UserCreateDTO,
    UserReadDTO,
    UserReadFullDTO,
    UserUpdateDTO,
)
from app.models import Category, TodoItem, User
from app.repositories import (
    CategoryRepository,
    TodoItemRepository,
    UserRepository,
    provide_category_repo,
    provide_todoitem_repo,
    provide_user_repo,
)


class ItemController(Controller):
    path = "/items"
    tags = ["items"]
    dependencies = {"todoitem_repo": provide_todoitem_repo}
    return_dto = TodoItemReadFullDTO

    @get()
    async def list_items(
        self, todoitem_repo: TodoItemRepository, done: bool | None = None
    ) -> Sequence[TodoItem]:
        if done is None:
            return todoitem_repo.list()
        else:
            return todoitem_repo.list(
                CollectionFilter(field_name="done", values=[done])
            )

    @get("/{item_id:int}")
    async def get_item(
        self, todoitem_repo: TodoItemRepository, item_id: int
    ) -> TodoItem:
        try:
            return todoitem_repo.get(item_id)
        except NotFoundError as e:
            raise NotFoundException(detail=f"Item {item_id} no encontrado") from e

    @post(
        dto=TodoItemCreateDTO,
        dependencies={
            "category_repo": provide_category_repo,
            "user_repo": provide_user_repo,
        },
    )
    async def add_item(
        self,
        todoitem_repo: TodoItemRepository,
        category_repo: CategoryRepository,
        user_repo: UserRepository,
        data: TodoItem,
    ) -> TodoItem:
        if data.user_id is not None:
            user = user_repo.get(data.user_id)
            if not user.enabled:
                raise HTTPException(status_code=400, detail="Usuario deshabilitado")
        data.categories = category_repo.list(
            CollectionFilter(field_name="id", values=[c.id for c in data.categories])
        )

        return todoitem_repo.add(data)

    @patch(
        "/{item_id:int}",
        dto=TodoItemUpdateDTO,
        dependencies={"category_repo": provide_category_repo},
    )
    async def update_item(
        self,
        todoitem_repo: TodoItemRepository,
        category_repo: CategoryRepository,
        item_id: int,
        data: DTOData[TodoItem],
    ) -> TodoItem:
        try:
            data_dict = data.as_builtins()
            if "categories" in data_dict:
                data_dict["categories"] = category_repo.list(
                    CollectionFilter(
                        field_name="id", values=[c.id for c in data_dict["categories"]]
                    )
                )
            if "done" in data_dict and data_dict["done"]:
                data_dict["completion"] = datetime.now()
            item, _ = todoitem_repo.get_and_update(
                id=item_id, match_fields=["id"], **data_dict
            )
            return item
        except NotFoundError as e:
            raise NotFoundException(detail=f"Item {item_id} no encontrado") from e

    @delete("/{item_id:int}")
    async def delete_item(
        self, todoitem_repo: TodoItemRepository, item_id: int
    ) -> None:
        try:
            todoitem_repo.delete(item_id)
        except NotFoundError as e:
            raise NotFoundException(detail=f"Item {item_id} no encontrado") from e


class CategoryController(Controller):
    path = "/categories"
    tags = ["categories"]
    return_dto = CategoryReadDTO
    dependencies = {"category_repo": provide_category_repo}

    @get("/")
    async def list_categories(
        self, category_repo: CategoryRepository
    ) -> list[Category]:
        return category_repo.list()

    @get("/{category_id:int}", return_dto=CategoryReadFullDTO)
    async def get_category(
        self, category_repo: CategoryRepository, category_id: int
    ) -> Category:
        try:
            return category_repo.get(category_id)
        except NotFoundError as e:
            raise NotFoundException(
                detail=f"Categoria con id={category_id} no encontrada"
            ) from e

    @post("/", dto=CategoryCreateDTO)
    async def add_category(
        self, category_repo: CategoryRepository, data: Category
    ) -> Category:
        return category_repo.add(data)

    @patch("/{category_id:int}", dto=CategoryUpdateDTO)
    async def update_category(
        self,
        category_repo: CategoryRepository,
        category_id: int,
        data: DTOData[Category],
    ) -> Category:
        try:
            category, _ = category_repo.get_and_update(
                id=category_id, **data.as_builtins(), match_fields=["id"]
            )
            return category
        except NotFoundError as e:
            raise NotFoundException(
                detail=f"Categoria {category_id} no encontrada"
            ) from e

    @delete("/{category_id:int}")
    async def delete_category(
        self, category_repo: CategoryRepository, category_id: int
    ) -> None:
        try:
            category_repo.delete(category_id)
        except NotFoundError as e:
            raise NotFoundException(
                detail=f"Categoria {category_id} no encontrada"
            ) from e


class UserController(Controller):
    path = "/users"
    tags = ["users"]
    return_dto = UserReadFullDTO
    dependencies = {"user_repo": provide_user_repo}

    @get("/", return_dto=UserReadDTO)
    async def list_users(self, user_repo: UserRepository) -> list[User]:
        return user_repo.list()

    @get("/{user_id:int}")
    async def get_user(self, user_repo: UserRepository, user_id: int) -> User:
        try:
            return user_repo.get(user_id)
        except NotFoundError as e:
            raise NotFoundException(detail=f"Usuario {user_id} no encontrado") from e

    @post("/", dto=UserCreateDTO)
    async def add_user(self, user_repo: UserRepository, data: User) -> User:
        return user_repo.add(data)

    @patch("/{user_id:int}", dto=UserUpdateDTO)
    async def update_user(
        self, user_repo: UserRepository, user_id: int, data: DTOData[User]
    ) -> User:
        try:
            user, _ = user_repo.get_and_update(
                id=user_id, **data.as_builtins(), match_fields=["id"]
            )
            return user
        except NotFoundError as e:
            raise NotFoundException(detail=f"Usuario {user_id} no encontrado") from e

    @delete("/{user_id:int}")
    async def delete_user(self, user_repo: UserRepository, user_id: int) -> None:
        try:
            user_repo.delete(user_id)
        except NotFoundError as e:
            raise NotFoundException(detail=f"Usuario {user_id} no encontrado") from e

    @get(
        "/{user_id:int}/items",
        return_dto=TodoItemReadDTO,
        dependencies={"todoitem_repo": provide_todoitem_repo},
    )
    async def get_user_items(
        self,
        todoitem_repo: TodoItemRepository,
        user_id: int,
        done: bool | None = None,
    ) -> list[TodoItem]:
        try:
            if done is None:
                return todoitem_repo.list(CollectionFilter(field_name="user_id", values=[user_id]))
            else:
                return todoitem_repo.list(
                    statement=select(TodoItem).where(
                        TodoItem.user_id == user_id, TodoItem.done == done
                    )
                )
        except NotFoundError as e:
            raise NotFoundException(detail=f"Usuario {user_id} no encontrado") from e
