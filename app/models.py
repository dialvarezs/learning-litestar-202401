from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class TodoItem(Base):
    __tablename__ = "todoitems"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    done: Mapped[bool]

    categories: Mapped[list["Category"]] = relationship(
        back_populates="items", secondary="todoitem_categories"
    )


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]

    items: Mapped[list["TodoItem"]] = relationship(
        back_populates="categories", secondary="todoitem_categories"
    )


class TodoItemCategories(Base):
    __tablename__ = "todoitem_categories"

    item_id: Mapped[int] = mapped_column(ForeignKey("todoitems.id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), primary_key=True
    )
