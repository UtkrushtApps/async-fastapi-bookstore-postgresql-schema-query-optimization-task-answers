from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from models import Book, Author, Category
from typing import Optional, List

# Add Book (already fully async in the new implementation)
async def add_book(session: AsyncSession, title: str, description: Optional[str], author_name: str, category_name: str):
    # Find or create author
    author_stmt = select(Author).where(Author.name == author_name)
    author_result = await session.execute(author_stmt)
    author = author_result.scalars().first()
    if not author:
        author = Author(name=author_name)
        session.add(author)
        await session.flush()  # assign id

    # Find or create category
    cat_stmt = select(Category).where(Category.name == category_name)
    cat_result = await session.execute(cat_stmt)
    category = cat_result.scalars().first()
    if not category:
        category = Category(name=category_name)
        session.add(category)
        await session.flush()
                    
    # Create book
    book = Book(title=title, description=description, author_id=author.id, category_id=category.id)
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book

# Get Book by ID
async def get_book(session: AsyncSession, book_id: int) -> Optional[Book]:
    stmt = select(Book).options(joinedload(Book.author), joinedload(Book.category)).where(Book.id == book_id)
    result = await session.execute(stmt)
    return result.scalars().first()

# Search Books by Author Name
async def get_books_by_author(session: AsyncSession, author_name: str) -> List[Book]:
    # Index on author.name and books.author_id used
    stmt = (
        select(Book)
        .join(Author)
        .options(joinedload(Book.author), joinedload(Book.category))
        .where(Author.name == author_name)
        .order_by(Book.id.desc())
    )
    result = await session.execute(stmt)
    return result.scalars().all()

# Search Books by Category Name
async def get_books_by_category(session: AsyncSession, category_name: str) -> List[Book]:
    stmt = (
        select(Book)
        .join(Category)
        .options(joinedload(Book.author), joinedload(Book.category))
        .where(Category.name == category_name)
        .order_by(Book.id.desc())
    )
    result = await session.execute(stmt)
    return result.scalars().all()

# List All Books
async def list_books(session: AsyncSession) -> List[Book]:
    stmt = select(Book).options(joinedload(Book.author), joinedload(Book.category)).order_by(Book.id.desc())
    res = await session.execute(stmt)
    return res.scalars().all()
