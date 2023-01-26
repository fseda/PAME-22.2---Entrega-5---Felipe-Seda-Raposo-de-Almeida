"""empty message

Revision ID: 212e21194838
Revises: 
Create Date: 2023-01-26 15:34:19.740577

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '212e21194838'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=20), nullable=True),
    sa.Column('cpf', sa.String(length=11), nullable=True),
    sa.Column('phone_number', sa.String(length=12), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('password_hash', sa.LargeBinary(length=128), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Appointment',
    sa.Column('pk_Appointment', sa.Integer(), nullable=False),
    sa.Column('start', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], name='fk_Appointment_id_User', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('pk_Appointment')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Appointment')
    op.drop_table('User')
    # ### end Alembic commands ###