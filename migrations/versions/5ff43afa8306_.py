"""empty message

Revision ID: 5ff43afa8306
Revises: dfdae831c960
Create Date: 2019-01-30 11:16:56.600463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ff43afa8306'
down_revision = 'dfdae831c960'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('donation')
    op.drop_index('ix_donationreason_end_date', table_name='donationreason')
    op.drop_index('ix_donationreason_timestamp', table_name='donationreason')
    op.drop_table('donationreason')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('donationreason',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('problem', sa.TEXT(), nullable=True),
    sa.Column('target_amount', sa.INTEGER(), nullable=True),
    sa.Column('author_id', sa.INTEGER(), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.Column('post_id', sa.INTEGER(), nullable=True),
    sa.Column('end_date', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_donationreason_timestamp', 'donationreason', ['timestamp'], unique=False)
    op.create_index('ix_donationreason_end_date', 'donationreason', ['end_date'], unique=False)
    op.create_table('donation',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('donation_id', sa.INTEGER(), nullable=False),
    sa.Column('amount', sa.INTEGER(), nullable=True),
    sa.Column('time_created', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['donation_id'], ['donationreason.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###