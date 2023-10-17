"""image_path

Revision ID: 9f0908883491
Revises: 2a300be76222
Create Date: 2023-10-17 22:47:20.240938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f0908883491'
down_revision = '2a300be76222'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_path', sa.String(length=255), nullable=False))
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=64),
               nullable=False)
        batch_op.alter_column('decription',
               existing_type=sa.VARCHAR(length=140),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.alter_column('decription',
               existing_type=sa.VARCHAR(length=140),
               nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=64),
               nullable=True)
        batch_op.drop_column('image_path')

    # ### end Alembic commands ###
