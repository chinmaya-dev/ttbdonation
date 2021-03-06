"""empty message

Revision ID: 1d6e95911778
Revises: 829813cf1f08
Create Date: 2019-01-22 15:24:38.777833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d6e95911778'
down_revision = '829813cf1f08'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('campaigncommentlikes')
    op.drop_index('ix_campaign_campaign_end_date', table_name='campaign')
    op.drop_index('ix_campaign_campaign_start_date', table_name='campaign')
    op.drop_table('campaign')
    op.drop_table('campaignsub')
    op.drop_index('ix_campaignbudget_timestamp', table_name='campaignbudget')
    op.drop_table('campaignbudget')
    op.drop_index('ix_campaigncomments_timestamp', table_name='campaigncomments')
    op.drop_table('campaigncomments')
    op.drop_table('campaignlikes')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('campaignlikes',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('campaign_id', sa.INTEGER(), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['campaign_id'], ['campaign.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('campaigncomments',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('body', sa.TEXT(), nullable=True),
    sa.Column('body_html', sa.TEXT(), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.Column('disabled', sa.BOOLEAN(), nullable=True),
    sa.Column('author_id', sa.INTEGER(), nullable=True),
    sa.Column('campaign_id', sa.INTEGER(), nullable=True),
    sa.CheckConstraint('disabled IN (0, 1)'),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['campaign_id'], ['campaign.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_campaigncomments_timestamp', 'campaigncomments', ['timestamp'], unique=False)
    op.create_table('campaignbudget',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('amount', sa.INTEGER(), nullable=True),
    sa.Column('author_id', sa.INTEGER(), nullable=False),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.Column('campaign_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['campaign_id'], ['campaign.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_campaignbudget_timestamp', 'campaignbudget', ['timestamp'], unique=False)
    op.create_table('campaignsub',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('campaign_id', sa.INTEGER(), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['campaign_id'], ['campaign.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('campaign',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('goal', sa.TEXT(), nullable=False),
    sa.Column('location', sa.VARCHAR(), nullable=False),
    sa.Column('language', sa.VARCHAR(), nullable=True),
    sa.Column('business_category', sa.VARCHAR(), nullable=True),
    sa.Column('service_category', sa.VARCHAR(), nullable=True),
    sa.Column('headline_1', sa.TEXT(), nullable=False),
    sa.Column('headline_2', sa.TEXT(), nullable=False),
    sa.Column('description', sa.VARCHAR(length=500), nullable=False),
    sa.Column('action', sa.TEXT(), nullable=True),
    sa.Column('campaign_start_date', sa.DATETIME(), nullable=True),
    sa.Column('campaign_end_date', sa.DATETIME(), nullable=True),
    sa.Column('target_age_range', sa.INTEGER(), nullable=True),
    sa.Column('sub_goals', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_campaign_campaign_start_date', 'campaign', ['campaign_start_date'], unique=False)
    op.create_index('ix_campaign_campaign_end_date', 'campaign', ['campaign_end_date'], unique=False)
    op.create_table('campaigncommentlikes',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('campaign_comment_id', sa.INTEGER(), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['campaign_comment_id'], ['campaigncomments.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
