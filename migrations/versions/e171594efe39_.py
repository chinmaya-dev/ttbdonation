"""empty message

Revision ID: e171594efe39
Revises: 457ddfed60e3
Create Date: 2019-03-10 14:26:19.130100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e171594efe39'
down_revision = '457ddfed60e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('socialdash', sa.Column('share', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('socialdash', 'share')
    # ### end Alembic commands ###
