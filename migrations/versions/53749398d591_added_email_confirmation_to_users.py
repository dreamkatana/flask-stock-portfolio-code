"""Added email confirmation to users

Revision ID: 53749398d591
Revises: 819538703899
Create Date: 2020-03-02 21:37:00.363356

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53749398d591'
down_revision = '819538703899'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email_confirmation_sent_on', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('email_confirmed', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('email_confirmed_on', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('registered_on', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'registered_on')
    op.drop_column('users', 'email_confirmed_on')
    op.drop_column('users', 'email_confirmed')
    op.drop_column('users', 'email_confirmation_sent_on')
    # ### end Alembic commands ###