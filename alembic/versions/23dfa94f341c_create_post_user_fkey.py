"""create post user fkey

Revision ID: 23dfa94f341c
Revises: e98f984d0eae
Create Date: 2022-10-11 10:08:24.219979

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '23dfa94f341c'
down_revision = 'e98f984d0eae'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fkey', source_table='posts', referent_table='users',
                          local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_column('posts', 'user_id')
    op.drop_constraint('posts_users_fkey', table_name='posts')
