"""empty message

Revision ID: 279d6663f9cf
Revises: b98a054a70f0
Create Date: 2019-02-27 19:41:42.890634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '279d6663f9cf'
down_revision = 'b98a054a70f0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blog', sa.Column('blog_youtube_tagline', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('blog', 'blog_youtube_tagline')
    # ### end Alembic commands ###
