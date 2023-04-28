"""generate user table

Revision ID: 950618907f04
Revises: 7ed6bfc4b036
Create Date: 2023-04-28 10:10:07.795413

"""
from uuid import uuid4
from datetime import datetime
from alembic import op
import sqlalchemy as sa
from schemas.user import get_password_hash
from settings import ADMIN_DEFAULT_PASSWORD


# revision identifiers, used by Alembic.
revision = '950618907f04'
down_revision = '7ed6bfc4b036'
branch_labels = None
depends_on = None
default_company_id = "8affc72f-a1d5-46d6-ad26-bacaa345cbb8"


def upgrade() -> None:
    # User Table
    user_table = op.create_table(
        "user",
        sa.Column("id", sa.String, nullable=False, primary_key=True),
        sa.Column("email", sa.String, unique=True, nullable=True, index=True),
        sa.Column("username", sa.String, unique=True, index=True),
        sa.Column("first_name", sa.String),
        sa.Column("last_name", sa.String),
        sa.Column("password", sa.String),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("is_admin", sa.Boolean, default=False),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
        sa.Column('company_id', sa.String, nullable=False),
        sa.ForeignKeyConstraint(['company_id'], ['company.id'],)
    )
    op.create_index("idx_usr_fst_lst_name", "user",
                    ["first_name", "last_name"])

    # Data seed for first user
    op.bulk_insert(user_table, [
        {
            "id": str(uuid4()),
            "email": "fastapi_tour@sample.com",
            "username": "fa_admin",
            "password": get_password_hash(ADMIN_DEFAULT_PASSWORD),
            "first_name": "FastApi",
            "last_name": "Admin",
            "is_active": True,
            "is_admin": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "company_id": default_company_id
        }
    ])


def downgrade() -> None:
    # Rollback foreign key
    op.drop_column("task", "user_id")
    # Rollback foreign key
    op.drop_table("user")
