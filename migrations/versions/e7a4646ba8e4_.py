"""empty message

Revision ID: e7a4646ba8e4
Revises: 8e246c6ab6cb
Create Date: 2025-03-16 11:03:49.839925

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7a4646ba8e4'
down_revision = '8e246c6ab6cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pothole', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pothole', schema=None) as batch_op:
        batch_op.drop_column('image')

    # ### end Alembic commands ###
