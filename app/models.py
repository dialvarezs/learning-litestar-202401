from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class TodoItem(Base):
    __tablename__ = "todoitems"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    done: Mapped[bool] = mapped_column(default=False, server_default="0")
    completion: Mapped[Optional[datetime]]
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))

    user: Mapped[Optional["User"]] = relationship(back_populates="items")
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


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    fullname: Mapped[str]
    enabled: Mapped[bool] = mapped_column(default=True, server_default="1")

    items: Mapped[list["TodoItem"]] = relationship(back_populates="user")
