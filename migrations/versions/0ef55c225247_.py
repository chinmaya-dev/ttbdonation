"""empty message

Revision ID: 0ef55c225247
Revises: 0555a7d55ab9
Create Date: 2019-02-17 07:04:48.609672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ef55c225247'
down_revision = '0555a7d55ab9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('event_type', sa.String(), nullable=True),
    sa.Column('event_name', sa.String(), nullable=True),
    sa.Column('event_category', sa.String(), nullable=True),
    sa.Column('event_description', sa.String(), nullable=True),
    sa.Column('image_file', sa.String(length=20), nullable=True),
    sa.Column('event_location', sa.String(), nullable=True),
    sa.Column('event_start_date', sa.DateTime(), nullable=True),
    sa.Column('event_end_date', sa.DateTime(), nullable=True),
    sa.Column('event_frequency', sa.String(), nullable=True),
    sa.Column('event_links', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_events_event_end_date'), 'events', ['event_end_date'], unique=False)
    op.create_index(op.f('ix_events_event_start_date'), 'events', ['event_start_date'], unique=False)
    op.create_table('eventsintrest',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('events_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['events_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('eventsintrest')
    op.drop_index(op.f('ix_events_event_start_date'), table_name='events')
    op.drop_index(op.f('ix_events_event_end_date'), table_name='events')
    op.drop_table('events')
    # ### end Alembic commands ###
