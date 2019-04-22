"""empty message

Revision ID: 58e42abe73de
Revises: d0f5fd66d70b
Create Date: 2019-01-31 11:55:08.452296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58e42abe73de'
down_revision = 'd0f5fd66d70b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Sponsorshipboost',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('action', sa.Text(), nullable=True),
    sa.Column('target_audience', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('sponsor_request_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sponsor_request_id'], ['sponsorshiprequest.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Sponsorshipboost_end_date'), 'Sponsorshipboost', ['end_date'], unique=False)
    op.create_index(op.f('ix_Sponsorshipboost_timestamp'), 'Sponsorshipboost', ['timestamp'], unique=False)
    op.create_table('campaignboost',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('action', sa.Text(), nullable=True),
    sa.Column('target_audience', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('campaign_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['campaign_id'], ['campaign.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_campaignboost_end_date'), 'campaignboost', ['end_date'], unique=False)
    op.create_index(op.f('ix_campaignboost_timestamp'), 'campaignboost', ['timestamp'], unique=False)
    op.create_table('postboost',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('action', sa.Text(), nullable=True),
    sa.Column('target_audience', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_postboost_end_date'), 'postboost', ['end_date'], unique=False)
    op.create_index(op.f('ix_postboost_timestamp'), 'postboost', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_postboost_timestamp'), table_name='postboost')
    op.drop_index(op.f('ix_postboost_end_date'), table_name='postboost')
    op.drop_table('postboost')
    op.drop_index(op.f('ix_campaignboost_timestamp'), table_name='campaignboost')
    op.drop_index(op.f('ix_campaignboost_end_date'), table_name='campaignboost')
    op.drop_table('campaignboost')
    op.drop_index(op.f('ix_Sponsorshipboost_timestamp'), table_name='Sponsorshipboost')
    op.drop_index(op.f('ix_Sponsorshipboost_end_date'), table_name='Sponsorshipboost')
    op.drop_table('Sponsorshipboost')
    # ### end Alembic commands ###
