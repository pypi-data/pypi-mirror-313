"""todo app database module."""

import pathlib
from datetime import datetime
from sqlalchemy import String, create_engine, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

app_dir = pathlib.Path.home() / ".pytodo"
app_dir.mkdir(exist_ok=True)


engine = create_engine(f"sqlite:///{app_dir}/todo_db.sqlite")
Session = sessionmaker(engine)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    create_date: Mapped[datetime] = mapped_column(insert_default=func.now())


class TodoUser(Base):
    """Todo user model."""

    __tablename__ = "todo_user"
    username: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    password_hash: Mapped[str]

    todos: Mapped[list["Todo"]] = relationship(back_populates="todo_user")


class Todo(Base):
    """Todo db model."""

    __tablename__ = "todo"
    # __table_args__ = (UniqueConstraint('user_id', 'title', 'done'),)
    user_id = mapped_column(ForeignKey("todo_user.id"))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    done: Mapped[bool]

    todo_user: Mapped["TodoUser"] = relationship(back_populates="todos")


def get_db():
    try:
        Base.metadata.create_all(engine)
        db = Session()
        return db
    finally:
        db.close()
