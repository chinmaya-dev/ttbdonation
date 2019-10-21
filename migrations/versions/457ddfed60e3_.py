"""empty message

Revision ID: 457ddfed60e3
Revises: 157f9d719e88
Create Date: 2019-03-10 14:18:39.277866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '457ddfed60e3'
down_revision = '157f9d719e88'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('socialdash',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('likes', sa.Integer(), nullable=True),
    sa.Column('views', sa.Integer(), nullable=True),
    sa.Column('comment', sa.Integer(), nullable=True),
    sa.Column('category', sa.Text(), nullable=True),
    sa.Column('engagments', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('socialdash')
    # ### end Alembic commands ###