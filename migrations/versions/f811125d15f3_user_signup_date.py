"""user signup_date

Revision ID: f811125d15f3
Revises: 8c6a3291dab9
Create Date: 2020-04-22 14:07:52.386688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f811125d15f3'
down_revision = '8c6a3291dab9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('signup_date', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'signup_date')
    # ### end Alembic commands ###
