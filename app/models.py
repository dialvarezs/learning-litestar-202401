from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TodoItem(Base):
    __tablename__ = "todoitems"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str]
    listo: Mapped[bool]
