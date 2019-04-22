"""dropdown 1

Revision ID: e3fd3a7be286
Revises: ca5e0cca2984
Create Date: 2018-12-17 04:20:33.914972

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3fd3a7be286'
down_revision = 'ca5e0cca2984'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role', sa.Text(), nullable=True),
    sa.Column('cat', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('sports', sa.Column('current_team', sa.Text(), nullable=True))
    op.add_column('user', sa.Column('issues', sa.String(length=60), nullable=True))
    op.add_column('user', sa.Column('support', sa.String(length=60), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'support')
    op.drop_column('user', 'issues')
    op.drop_column('sports', 'current_team')
    op.drop_table('categories')
    # ### end Alembic commands ###
