"""create posts table

Revision ID: 4422275122ec
Revises: 
Create Date: 2022-10-10 20:29:21.946827

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4422275122ec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text('now()')),
                    )


def downgrade() -> None:
    op.drop_table('posts')
