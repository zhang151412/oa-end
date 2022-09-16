"""empty message

Revision ID: d375e5fd3a48
Revises: 
Create Date: 2022-09-15 16:19:08.219340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd375e5fd3a48'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('oa_user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('jobnumber', sa.String(length=100), nullable=False),
    sa.Column('realname', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('_password', sa.String(length=200), nullable=False),
    sa.Column('join_time', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_leader', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('jobnumber')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('oa_user')
    # ### end Alembic commands ###
