"""db index and address

Revision ID: 52a1d7766d41
Revises: aed888d7bd08
Create Date: 2023-10-12 14:38:53.773264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "52a1d7766d41"
down_revision = "aed888d7bd08"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("dogs", sa.Column("address", sa.String(length=250), nullable=False))
    op.create_index(op.f("ix_dogs_age_months"), "dogs", ["age_months"], unique=False)
    op.add_column(
        "users",
        sa.Column("is_admin", sa.Boolean(), server_default="FALSE", nullable=False),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "is_admin")
    op.drop_index(op.f("ix_dogs_age_months"), table_name="dogs")
    op.drop_column("dogs", "address")
    # ### end Alembic commands ###