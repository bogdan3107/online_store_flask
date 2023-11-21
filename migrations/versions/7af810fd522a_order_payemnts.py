"""order payemnts

Revision ID: 7af810fd522a
Revises: d826935281f7
Create Date: 2023-11-21 17:24:49.734413

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7af810fd522a'
down_revision = 'd826935281f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('payment_type', sa.String(length=32), nullable=True))
        batch_op.add_column(sa.Column('payment_status', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.drop_column('payment_status')
        batch_op.drop_column('payment_type')

    # ### end Alembic commands ###
