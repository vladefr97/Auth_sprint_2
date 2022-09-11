"""init

Revision ID: a6afdc1acb25
Revises: 
Create Date: 2022-09-11 18:42:15.582497

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a6afdc1acb25'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE SCHEMA IF NOT EXISTS auth")

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('role_type', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    schema='auth'
    )
    op.create_table('user',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('user_role', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['user_role'], ['auth.role.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('login'),
    schema='auth'
    )
    op.create_table('social_account',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('social_id', sa.String(length=100), nullable=False),
    sa.Column('social_name', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['auth.user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('social_id', 'social_name'),
    schema='auth'
    )
    op.create_table('user_history',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_agent', sa.Text(), nullable=False),
    sa.Column('ip_address', sa.String(length=20), nullable=False),
    sa.Column('url', sa.Text(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['auth.user.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    schema='auth'
    )
    # ### end Alembic commands ###


def downgrade():
    op.execute("drop schema if exists auth cascade;")