"""empty message

Revision ID: 0555a7d55ab9
Revises: 14e7f2421742
Create Date: 2019-02-17 06:41:08.454948

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0555a7d55ab9'
down_revision = '14e7f2421742'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_events_event_end_date', table_name='events')
    op.drop_index('ix_events_event_start_date', table_name='events')
    op.drop_table('events')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('event_name', sa.VARCHAR(), nullable=True),
    sa.Column('event_description', sa.VARCHAR(), nullable=True),
    sa.Column('event_location', sa.VARCHAR(), nullable=True),
    sa.Column('event_start_date', sa.DATETIME(), nullable=True),
    sa.Column('event_end_date', sa.DATETIME(), nullable=True),
    sa.Column('event_status', sa.BOOLEAN(), nullable=True),
    sa.CheckConstraint('event_status IN (0, 1)'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_events_event_start_date', 'events', ['event_start_date'], unique=False)
    op.create_index('ix_events_event_end_date', 'events', ['event_end_date'], unique=False)
    # ### end Alembic commands ###
