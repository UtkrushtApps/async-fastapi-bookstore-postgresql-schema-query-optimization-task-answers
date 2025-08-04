from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_index('ix_authors_name', 'authors', ['name'], unique=True)
    op.create_index('ix_categories_name', 'categories', ['name'], unique=True)
    op.create_index('ix_books_author_id', 'books', ['author_id'])
    op.create_index('ix_books_category_id', 'books', ['category_id'])
    op.create_unique_constraint('uq_title_author', 'books', ['title', 'author_id'])

def downgrade():
    op.drop_constraint('uq_title_author', 'books', type_='unique')
    op.drop_index('ix_books_category_id', table_name='books')
    op.drop_index('ix_books_author_id', table_name='books')
    op.drop_index('ix_categories_name', table_name='categories')
    op.drop_index('ix_authors_name', table_name='authors')
