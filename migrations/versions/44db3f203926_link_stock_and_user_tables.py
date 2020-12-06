"""link stock and user tables

Revision ID: 44db3f203926
Revises: de71046acd2f
Create Date: 2020-12-06 09:37:24.515328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44db3f203926'
down_revision = 'de71046acd2f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stocks', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'stocks', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'stocks', type_='foreignkey')
    op.drop_column('stocks', 'user_id')
    # ### end Alembic commands ###
