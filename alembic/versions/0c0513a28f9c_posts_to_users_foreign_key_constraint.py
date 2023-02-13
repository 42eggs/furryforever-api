"""posts to users foreign key constraint

Revision ID: 0c0513a28f9c
Revises: 3f058dacea79
Create Date: 2023-02-12 16:32:17.183410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0c0513a28f9c"
down_revision = "3f058dacea79"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_foreign_key(
        "posts_users_fkey",
        source_table="posts",
        referent_table="users",
        local_cols=["user_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fkey", source_table="posts", type_="foreignkey")
    pass
