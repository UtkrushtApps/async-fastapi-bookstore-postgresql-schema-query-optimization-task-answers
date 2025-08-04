# Solution Steps

1. Define proper relationships and unique/index constraints in SQLAlchemy models (models.py): add unique indexes for author and category names, set up foreign key indexes and relationship loading.

2. Add or update Alembic migration to ensure all relevant indexes and unique constraints are in the PostgreSQL schema for fast lookups.

3. Update database.py to use SQLAlchemy's async engine and async sessionmaker. Provide a dependency that yields an async session.

4. Go through all CRUD/query functions in crud.py: ensure every DB interaction is fully asynchronous, using await/async session (AsyncSession) methods.

5. Optimize lookups in search-by-author and search-by-category queries: use joins and ensure joinedload eager loading for related entities to minimize roundtrips. Order results for determinism.

6. Ensure that all queries by author or category perform lookups using indexed columns (author.name, category.name, books.author_id, books.category_id) and that DB access is non-blocking.

7. Test endpoints (e.g., /books/by-author, /books/by-category) to confirm response time is fast (under one second) and EXPLAIN plans use indexes.

8. Verify Alembic migrations apply cleanly and check resulting DB schema for new and correct indexes.

