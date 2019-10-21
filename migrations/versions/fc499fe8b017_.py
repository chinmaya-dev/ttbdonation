"""empty message

Revision ID: fc499fe8b017
Revises: 1d6e95911778
Create Date: 2019-01-22 15:25:31.571661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc499fe8b017'
down_revision = '1d6e95911778'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('campaign',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('goal', sa.Text(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('language', sa.String(), nullable=True),
    sa.Column('business_category', sa.String(), nullable=True),
    sa.Column('service_category', sa.String(), nullable=True),
    sa.Column('headline_1', sa.Text(), nullable=False),
    sa.Column('headline_2', sa.Text(), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=False),
    sa.Column('action', sa.Text(), nullable=True),
    sa.Column('campaign_start_date', sa.DateTime(), nullable=True),
    sa.Column('campaign_end_date', sa.DateTime(), nullable=True),
    sa.Column('target_age_range', sa.Integer(), nullable=True),
    sa.Column('sub_goals', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_campaign_campaign_end_date'), 'campaign', ['campaign_end_date'], unique=False)
    op.create_index(op.f('ix_campaign_campaign_start_date'), 'campaign', ['campaign_start_date'], unique=False)
    op.create_table('campaignbudget',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('campaign_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['campaign_id'], ['campaign.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_campaignbudget_timestamp'), 'campaignbudget', ['timestamp'], unique=False)
    op.create_table('campaigncomments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('body_html', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('campaign_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['campaign_id'], ['campaign.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_campaigncomments_timestamp'), 'campaigncomments', ['timestamp'], unique=False)
    op.create_table('campaignlikes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('campaign_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['campaign_id'], ['campaign.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('campaignsub',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('campaign_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['campaign_id'], ['campaign.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('campaigncommentlikes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('campaign_comment_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['campaign_comment_id'], ['campaigncomments.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('campaigncommentlikes')
    op.drop_table('campaignsub')
    op.drop_table('campaignlikes')
    op.drop_index(op.f('ix_campaigncomments_timestamp'), table_name='campaigncomments')
    op.drop_table('campaigncomments')
    op.drop_index(op.f('ix_campaignbudget_timestamp'), table_name='campaignbudget')
    op.drop_table('campaignbudget')
    op.drop_index(op.f('ix_campaign_campaign_start_date'), table_name='campaign')
    op.drop_index(op.f('ix_campaign_campaign_end_date'), table_name='campaign')
    op.drop_table('campaign')
    # ### end Alembic commands ###