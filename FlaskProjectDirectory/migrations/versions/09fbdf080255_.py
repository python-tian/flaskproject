"""empty message

Revision ID: 09fbdf080255
Revises: 8d8e081922c8
Create Date: 2019-08-18 15:28:14.637955

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09fbdf080255'
down_revision = '8d8e081922c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students', sa.Column('has_school', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('students', 'has_school')
    # ### end Alembic commands ###
