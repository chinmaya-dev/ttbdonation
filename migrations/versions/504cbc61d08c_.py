"""empty message

Revision ID: 504cbc61d08c
Revises: 32f8d4a2c957
Create Date: 2019-02-04 19:39:27.315653

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '504cbc61d08c'
down_revision = '32f8d4a2c957'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sponsorship', sa.Column('image_file', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sponsorship', 'image_file')
    # ### end Alembic commands ###
