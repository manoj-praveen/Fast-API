"""create users table

Revision ID: e98f984d0eae
Revises: 4422275122ec
Create Date: 2022-10-11 09:45:05.327216

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'e98f984d0eae'
down_revision = '4422275122ec'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('email_id', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text('now()')),
                    sa.UniqueConstraint('email_id')
                    )


def downgrade() -> None:
    op.drop_table('users')
