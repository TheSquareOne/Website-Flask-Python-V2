"""user edit_date

Revision ID: 8c6a3291dab9
Revises: 108fc55eb446
Create Date: 2020-04-22 14:07:11.704454

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c6a3291dab9'
down_revision = '108fc55eb446'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('edit_date', sa.TIMESTAMP(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'edit_date')
    # ### end Alembic commands ###