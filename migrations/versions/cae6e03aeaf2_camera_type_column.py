"""camera type column

Revision ID: cae6e03aeaf2
Revises: 4918f1fb5251
Create Date: 2024-06-26 18:47:30.073329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cae6e03aeaf2'
down_revision = '4918f1fb5251'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('camera', schema=None) as batch_op:
        batch_op.add_column(sa.Column('camera_type', sa.String(length=6), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('camera', schema=None) as batch_op:
        batch_op.drop_column('camera_type')

    # ### end Alembic commands ###