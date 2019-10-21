"""empty message

Revision ID: f84465370379
Revises: e171594efe39
Create Date: 2019-04-02 20:08:50.710148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f84465370379'
down_revision = 'e171594efe39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('image_file', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'image_file')
    # ### end Alembic commands ###