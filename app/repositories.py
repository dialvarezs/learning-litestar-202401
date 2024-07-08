from advanced_alchemy.repository import SQLAlchemySyncRepository
from sqlalchemy.orm import Session

from app.models import Category, TodoItem


class TodoItemRepository(SQLAlchemySyncRepository[TodoItem]):  # type: ignore
    model_type = TodoItem


async def provide_todoitem_repo(db_session: Session) -> TodoItemRepository:
    return TodoItemRepository(session=db_session, auto_commit=True)


class CategoryRepository(SQLAlchemySyncRepository[Category]):  # type: ignore
    model_type = Category


async def provide_category_repo(db_session: Session) -> CategoryRepository:
    return CategoryRepository(session=db_session, auto_commit=True)
