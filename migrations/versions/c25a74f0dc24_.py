"""empty message

Revision ID: c25a74f0dc24
Revises: 4bff2929db75
Create Date: 2019-01-26 06:47:35.464109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c25a74f0dc24'
down_revision = '4bff2929db75'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sponsorship',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('network', sa.String(), nullable=True),
    sa.Column('concept', sa.String(), nullable=True),
    sa.Column('product_link', sa.String(), nullable=True),
    sa.Column('target_category', sa.String(), nullable=True),
    sa.Column('type_infu', sa.String(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('payment_mode', sa.String(), nullable=True),
    sa.Column('price_range', sa.String(), nullable=True),
    sa.Column('duration', sa.String(), nullable=True),
    sa.Column('target_age_range', sa.String(), nullable=True),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('target_gender', sa.String(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sponsorship_end_date'), 'sponsorship', ['end_date'], unique=False)
    op.create_index(op.f('ix_sponsorship_start_date'), 'sponsorship', ['start_date'], unique=False)
    op.create_table('sponsorshipapply',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('network', sa.Text(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('concept', sa.Text(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('sponsor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sponsor_id'], ['sponsorship.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sponsorshipapply_timestamp'), 'sponsorshipapply', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_sponsorshipapply_timestamp'), table_name='sponsorshipapply')
    op.drop_table('sponsorshipapply')
    op.drop_index(op.f('ix_sponsorship_start_date'), table_name='sponsorship')
    op.drop_index(op.f('ix_sponsorship_end_date'), table_name='sponsorship')
    op.drop_table('sponsorship')
    # ### end Alembic commands ###
