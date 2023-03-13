"""add_validity_type

Revision ID: f2db3848bffd
Revises: 5c26094a1f43
Create Date: 2023-03-13 16:07:15.651017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2db3848bffd'
down_revision = '5c26094a1f43'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tbl_membership', sa.Column('validity_type', sa.String(), server_default='days', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tbl_membership', 'validity_type')
    # ### end Alembic commands ###
