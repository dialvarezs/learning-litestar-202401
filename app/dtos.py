from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig

from app.models import Category, TodoItem


class TodoItemReadDTO(SQLAlchemyDTO[TodoItem]):
    pass


class TodoItemCreateDTO(SQLAlchemyDTO[TodoItem]):
    config = SQLAlchemyDTOConfig(
        exclude={"id", "categories.0.name", "categories.0.description"}
    )


class TodoItemUpdateDTO(SQLAlchemyDTO[TodoItem]):
    config = SQLAlchemyDTOConfig(
        exclude={"id", "categories.0.name", "categories.0.description"}, partial=True
    )


class CategoryReadDTO(SQLAlchemyDTO[Category]):
    config = SQLAlchemyDTOConfig(exclude={"items"})


class CategoryReadFullDTO(SQLAlchemyDTO[Category]):
    pass


class CategoryCreateDTO(SQLAlchemyDTO[Category]):
    config = SQLAlchemyDTOConfig(exclude={"id", "items"})


class CategoryUpdateDTO(SQLAlchemyDTO[Category]):
    config = SQLAlchemyDTOConfig(exclude={"id", "items"}, partial=True)
