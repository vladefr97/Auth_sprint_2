"""partition

Revision ID: 2219be095f45
Revises: 4ecf5bed8c8e
Create Date: 2022-09-10 22:30:54.711647

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2219be095f45'
down_revision = '4ecf5bed8c8e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user_history_temp',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_agent', sa.Text(), nullable=False),
    sa.Column('ip_address', sa.String(length=20), nullable=False),
    sa.Column('url', sa.Text(), nullable=False),
    sa.Column('timestamp', sa.Integer),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.PrimaryKeyConstraint('id', 'timestamp'),
    sa.UniqueConstraint('id', 'timestamp'),

    schema='auth',
    postgresql_partition_by='RANGE (timestamp)'
    )
    op.execute("CREATE TABLE auth.user_history_y2022 (LIKE auth.user_history_temp INCLUDING DEFAULTS  INCLUDING  CONSTRAINTS)")

    op.execute("""
           INSERT INTO auth.user_history_temp (id, user_id, user_agent, ip_address, timestamp, url)
               SELECT id, user_id, user_agent, ip_address, timestamp, url
               FROM auth.user_history t where timestamp between '2022-01-01' and '2023-01-01';
       """)
    op.execute("""
           DELETE FROM auth.user_history where timestamp between '2022-01-01' and '2023-01-01';
       """)
    op.execute("ALTER TABLE auth.user_history_temp ATTACH PARTITION auth.user_history_y2022  values from ('2022-01-01') to ('2023-01-01')")


def downgrade():
    pass