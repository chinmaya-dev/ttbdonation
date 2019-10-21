"""empty message

Revision ID: 3ad7ce169b46
Revises: c86936a066d1
Create Date: 2019-03-04 16:56:27.904961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ad7ce169b46'
down_revision = 'c86936a066d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rewards', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_rewards_timestamp'), 'rewards', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_rewards_timestamp'), table_name='rewards')
    op.drop_column('rewards', 'timestamp')
    # ### end Alembic commands ###