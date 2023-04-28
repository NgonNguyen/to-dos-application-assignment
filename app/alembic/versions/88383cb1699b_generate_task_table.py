"""generate task table

Revision ID: 88383cb1699b
Revises: 950618907f04
Create Date: 2023-04-28 10:13:48.873532

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88383cb1699b'
down_revision = '950618907f04'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'task',
        sa.Column('id', sa.String, nullable=False, primary_key=True),
        sa.Column('summary', sa.String, nullable=False),
        sa.Column('description', sa.String),
        sa.Column('status', sa.String),
        sa.Column('priority', sa.String),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('user_id', sa.String),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'],)
    )


def downgrade() -> None:
    op.drop_table('task')
