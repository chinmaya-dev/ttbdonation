"""empty message

Revision ID: d9d9cc8c2bbf
Revises: 942ab33b9e92
Create Date: 2019-01-05 02:53:00.080934

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9d9cc8c2bbf'
down_revision = '942ab33b9e92'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('brand_name', sa.String(length=60), nullable=True))
    op.add_column('user', sa.Column('company_name', sa.String(length=60), nullable=True))
    op.add_column('user', sa.Column('role_in_brand', sa.String(length=60), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'role_in_brand')
    op.drop_column('user', 'company_name')
    op.drop_column('user', 'brand_name')
    # ### end Alembic commands ###
