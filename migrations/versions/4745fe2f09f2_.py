"""empty message

Revision ID: 4745fe2f09f2
Revises: 2936d5642701
Create Date: 2019-01-16 20:51:17.351351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4745fe2f09f2'
down_revision = '2936d5642701'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sponsershipcommentlikes')
    op.drop_table('sponsershiplikes')
    op.drop_table('sponsershipapply')
    op.drop_index('ix_sponsershipcomments_timestamp', table_name='sponsershipcomments')
    op.drop_table('sponsershipcomments')
    op.drop_table('sponsership')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sponsership',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('network', sa.VARCHAR(), nullable=True),
    sa.Column('product_link', sa.VARCHAR(), nullable=False),
    sa.Column('details', sa.VARCHAR(), nullable=False),
    sa.Column('category', sa.TEXT(), nullable=False),
    sa.Column('price_range', sa.TEXT(), nullable=False),
    sa.Column('deadline', sa.DATETIME(), nullable=False),
    sa.Column('sponsership_date_posted', sa.DATETIME(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sponsershipcomments',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('body', sa.TEXT(), nullable=True),
    sa.Column('body_html', sa.TEXT(), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.Column('disabled', sa.BOOLEAN(), nullable=True),
    sa.Column('author_id', sa.INTEGER(), nullable=True),
    sa.Column('sponsership_id', sa.INTEGER(), nullable=True),
    sa.CheckConstraint('disabled IN (0, 1)'),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sponsership_id'], ['sponsership.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_sponsershipcomments_timestamp', 'sponsershipcomments', ['timestamp'], unique=False)
    op.create_table('sponsershipapply',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('sponsership_id', sa.INTEGER(), nullable=True),
    sa.Column('social_id', sa.TEXT(), nullable=True),
    sa.Column('price', sa.TEXT(), nullable=True),
    sa.Column('concept', sa.TEXT(), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['sponsership_id'], ['sponsership.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sponsershiplikes',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('sponsership_id', sa.INTEGER(), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['sponsership_id'], ['sponsership.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sponsershipcommentlikes',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('sponsership_comment_id', sa.INTEGER(), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['sponsership_comment_id'], ['sponsershipcomments.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
