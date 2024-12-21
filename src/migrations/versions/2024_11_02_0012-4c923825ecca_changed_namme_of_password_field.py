"""changed namme of password field

Revision ID: 4c923825ecca
Revises: 69d8a6614ac6
Create Date: 2024-11-02 00:12:10.920298

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4c923825ecca"
down_revision: Union[str, None] = "69d8a6614ac6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users", sa.Column("hashed_password", sa.String(length=100), nullable=False)
    )
    op.drop_column("users", "password")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column(
            "password", sa.VARCHAR(length=100), autoincrement=False, nullable=False
        ),
    )
    op.drop_column("users", "hashed_password")
    # ### end Alembic commands ###