"""empty message

Revision ID: 99aa0341d08b
Revises: 053c757c7d40
Create Date: 2019-01-28 12:06:16.190888

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99aa0341d08b'
down_revision = '053c757c7d40'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('campaign', sa.Column('ad_format', sa.String(), nullable=True))
    op.add_column('campaign', sa.Column('links', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('campaign', 'links')
    op.drop_column('campaign', 'ad_format')
    # ### end Alembic commands ###
