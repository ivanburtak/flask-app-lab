"""Insert data into products table

Revision ID: f5afc5c8b3d0
Revises: f203922dfbcd
Create Date: 2025-11-30 00:15:34.705330

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import column, table

# revision identifiers, used by Alembic.
revision = 'f5afc5c8b3d0'
down_revision = 'f203922dfbcd'
branch_labels = None
depends_on = None


def upgrade():
    categories_table = table('categories', column('id', sa.Integer), column('name', sa.String))

    products_table = table('products',
                           column('name', sa.String),
                           column('price', sa.Float),
                           column('active', sa.Boolean),
                           column('category_id', sa.Integer)
                           )

    op.bulk_insert(categories_table, [
        {'name': 'Electronics'},
        {'name': 'Books'},
        {'name': 'Clothing'}
    ])

    op.bulk_insert(products_table, [
        {'name': 'Laptop', 'price': 1200.0, 'active': True, 'category_id': 1},
        {'name': 'Smartphone', 'price': 800.0, 'active': True, 'category_id': 1},
        {'name': 'Novel', 'price': 20.0, 'active': True, 'category_id': 2},
        {'name': 'T-Shirt', 'price': 25.0, 'active': False, 'category_id': 3},
    ])


def downgrade():
    op.execute("""
        DELETE FROM products
        WHERE name IN ('Laptop', 'Smartphone', 'Novel', 'T-Shirt');
    """)

    op.execute("""
        DELETE FROM categories
        WHERE name IN ('Electronics', 'Books', 'Clothing');
    """)
