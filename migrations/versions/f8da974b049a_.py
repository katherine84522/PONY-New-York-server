"""empty message

Revision ID: f8da974b049a
Revises: 0d00b5b419c8
Create Date: 2023-01-17 15:19:05.675219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8da974b049a'
down_revision = '0d00b5b419c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('protectors', schema=None) as batch_op:
        batch_op.drop_column('created_at')
        batch_op.drop_column('background_check')
        batch_op.drop_column('active')
        batch_op.drop_column('phone_number')
        batch_op.drop_column('rating')
        batch_op.drop_column('password')
        batch_op.drop_column('gender_identity')
        batch_op.drop_column('address')
        batch_op.drop_column('picture')
        batch_op.drop_column('updated_at')

    with op.batch_alter_table('requests', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', sa.String(length=1000), nullable=True))
        batch_op.add_column(sa.Column('time', sa.String(length=1000), nullable=True))
        batch_op.drop_column('datetime')

    with op.batch_alter_table('walkees', schema=None) as batch_op:
        batch_op.drop_column('created_at')
        batch_op.drop_column('phone_number')
        batch_op.drop_column('password')
        batch_op.drop_column('gender_identity')
        batch_op.drop_column('picture')
        batch_op.drop_column('updated_at')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('walkees', schema=None) as batch_op:
        batch_op.add_column(sa.Column('updated_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
        batch_op.add_column(sa.Column('picture', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('gender_identity', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('password', sa.VARCHAR(length=120), nullable=True))
        batch_op.add_column(sa.Column('phone_number', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))

    with op.batch_alter_table('requests', schema=None) as batch_op:
        batch_op.add_column(sa.Column('datetime', sa.DATETIME(), nullable=True))
        batch_op.drop_column('time')
        batch_op.drop_column('date')

    with op.batch_alter_table('protectors', schema=None) as batch_op:
        batch_op.add_column(sa.Column('updated_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
        batch_op.add_column(sa.Column('picture', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('address', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('gender_identity', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('password', sa.VARCHAR(length=120), nullable=True))
        batch_op.add_column(sa.Column('rating', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('phone_number', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('active', sa.BOOLEAN(), nullable=True))
        batch_op.add_column(sa.Column('background_check', sa.BOOLEAN(), nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))

    # ### end Alembic commands ###
