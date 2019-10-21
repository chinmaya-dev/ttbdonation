"""empty message

Revision ID: ac78a6549ab0
Revises: 378da180932d
Create Date: 2019-04-13 04:41:26.255398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac78a6549ab0'
down_revision = '378da180932d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('goal', sa.Text(), nullable=True),
    sa.Column('hurdles', sa.Text(), nullable=True),
    sa.Column('rank', sa.Text(), nullable=True),
    sa.Column('accomplished', sa.Text(), nullable=True),
    sa.Column('fear', sa.Text(), nullable=True),
    sa.Column('finance', sa.Text(), nullable=True),
    sa.Column('other', sa.Text(), nullable=True),
    sa.Column('motivate', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bio_timestamp'), 'bio', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_bio_timestamp'), table_name='bio')
    op.drop_table('bio')
    # ### end Alembic commands ###