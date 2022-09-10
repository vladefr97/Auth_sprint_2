"""initial

Revision ID: 4ecf5bed8c8e
Revises: 
Create Date: 2022-09-10 22:13:20.115973

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4ecf5bed8c8e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE SCHEMA IF NOT EXISTS auth")
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('role_type', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('role_type'),
    schema='auth'
    )
    op.create_table('user',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('user_role', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['user_role'], ['auth.role.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('login'),
    schema='auth'
    )
    op.create_table('user_history',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_agent', sa.Text(), nullable=False),
    sa.Column('ip_address', sa.String(length=20), nullable=False),
    sa.Column('url', sa.Text(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['auth.user.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    schema='auth',

    )
    # ### end Alembic commands ###


def downgrade():
    op.execute("drop schema if exists auth cascade;")