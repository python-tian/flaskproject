"""empty message

Revision ID: b625d89915cc
Revises: 09fbdf080255
Create Date: 2019-08-18 17:19:49.477878

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b625d89915cc'
down_revision = '09fbdf080255'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ask', sa.Column('subtime', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ask', 'subtime')
    # ### end Alembic commands ###
