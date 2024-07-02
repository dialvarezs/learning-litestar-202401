from advanced_alchemy.repository import SQLAlchemySyncRepository
from sqlalchemy.orm import Session

from app.models import TodoItem


class TodoItemRepository(SQLAlchemySyncRepository[TodoItem]): # type: ignore
    model_type = TodoItem


async def provide_todoitem_repo(db_session: Session) -> TodoItemRepository:
    return TodoItemRepository(session=db_session, auto_commit=True)
