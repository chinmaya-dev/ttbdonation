"""empty message

Revision ID: 8e2332153682
Revises: 1d9f6375ed46
Create Date: 2019-02-05 20:01:11.307307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e2332153682'
down_revision = '1d9f6375ed46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('donationreason',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category', sa.Text(), nullable=True),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('image_file', sa.String(length=20), nullable=True),
    sa.Column('goal', sa.Text(), nullable=True),
    sa.Column('target_amount', sa.Integer(), nullable=True),
    sa.Column('amount_prefilled', sa.Integer(), nullable=True),
    sa.Column('end_method', sa.Text(), nullable=True),
    sa.Column('link', sa.Text(), nullable=True),
    sa.Column('country', sa.Text(), nullable=True),
    sa.Column('address', sa.Text(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_donationreason_end_date'), 'donationreason', ['end_date'], unique=False)
    op.create_index(op.f('ix_donationreason_start_date'), 'donationreason', ['start_date'], unique=False)
    op.create_table('donation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('donation_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('time_created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['donation_id'], ['donationreason.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('donation')
    op.drop_index(op.f('ix_donationreason_start_date'), table_name='donationreason')
    op.drop_index(op.f('ix_donationreason_end_date'), table_name='donationreason')
    op.drop_table('donationreason')
    # ### end Alembic commands ###
