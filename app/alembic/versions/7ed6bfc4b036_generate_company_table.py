"""generate company table

Revision ID: 7ed6bfc4b036
Revises: 
Create Date: 2023-04-28 10:06:38.289630

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa
from schemas.company import CompanyMode


# revision identifiers, used by Alembic.
revision = '7ed6bfc4b036'
down_revision = None
branch_labels = None
depends_on = None
default_company_id = "8affc72f-a1d5-46d6-ad26-bacaa345cbb8"


def upgrade() -> None:
    company_table = op.create_table(
        'company',
        sa.Column('id', sa.String, nullable=False, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String),
        sa.Column('mode', sa.Enum(CompanyMode),
                  nullable=False, default=CompanyMode.PRODUCT),
        sa.Column('rating', sa.SmallInteger)
    )

    # Data seed for first user
    op.bulk_insert(company_table, [
        {
            "id": default_company_id,
            "name": "Company a",
            "description": "This is description of company a",
            "mode": CompanyMode.PRODUCT,
            "rating": 5,
        }
    ])


def downgrade() -> None:
    # Rollback foreign key
    op.drop_column("user", "company_id")
    # Rollback foreign key
    op.drop_table('company')
