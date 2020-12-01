"""analytics

Revision ID: 5f40ff2de25d
Revises: 13942d305af1
Create Date: 2020-11-30 22:13:33.149176

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f40ff2de25d'
down_revision = '13942d305af1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('page_view',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('domain', sa.Text(), nullable=True),
    sa.Column('url', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('ip', sa.String(length=15), nullable=True),
    sa.Column('referrer', sa.Text(), nullable=True),
    sa.Column('headers', sa.JSON(), nullable=True),
    sa.Column('params', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('page_view', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_page_view_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('page_view', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_page_view_timestamp'))

    op.drop_table('page_view')
    # ### end Alembic commands ###