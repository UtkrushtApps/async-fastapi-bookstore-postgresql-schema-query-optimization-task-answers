from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint, Index, Text

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    books: Mapped[list["Book"]] = relationship("Book", back_populates="author", cascade='all, delete-orphan')

    def __repr__(self):
        return f"Author(id={self.id}, name={self.name})"

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False, unique=True, index=True)
    books: Mapped[list["Book"]] = relationship("Book", back_populates="category", cascade='all, delete-orphan')

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name})"

class Book(Base):
    __tablename__ = "books"
    __table_args__ = (
        UniqueConstraint("title", "author_id", name="uq_title_author"),
        Index("ix_books_author_id", "author_id"),
        Index("ix_books_category_id", "category_id"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), nullable=False, index=True)

    author: Mapped["Author"] = relationship("Author", back_populates="books")
    category: Mapped["Category"] = relationship("Category", back_populates="books")

    def __repr__(self):
        return f"Book(id={self.id}, title={self.title}, author_id={self.author_id}, category_id={self.category_id})"
