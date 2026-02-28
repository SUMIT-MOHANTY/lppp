"""Initial schema"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False), sa.Column('username', sa.String(50), nullable=False), sa.Column('email', sa.String(100), nullable=False), sa.Column('password_hash', sa.String(255), nullable=False), sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True), sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True), sa.Column('is_active', sa.Boolean(), nullable=True), sa.PrimaryKeyConstraint('id'))
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('structured_data', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False), sa.Column('user_id', sa.Integer(), nullable=False), sa.Column('data_type', sa.String(50), nullable=False), sa.Column('payload', postgresql.JSON(astext_type=sa.Text()), nullable=False), sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True), sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True), sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True), sa.ForeignKeyConstraint(['user_id'], ['users.id'], ), sa.PrimaryKeyConstraint('id'))
    op.create_index(op.f('ix_structured_data_created_at'), 'structured_data', ['created_at'], unique=False)
    op.create_index(op.f('ix_structured_data_data_type'), 'structured_data', ['data_type'], unique=False)
    op.create_index(op.f('ix_structured_data_user_id'), 'structured_data', ['user_id'], unique=False)
    op.create_table('api_logs', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False), sa.Column('user_id', sa.Integer(), nullable=True), sa.Column('endpoint', sa.String(255), nullable=False), sa.Column('method', sa.String(10), nullable=False), sa.Column('request_body', postgresql.JSON(astext_type=sa.Text()), nullable=True), sa.Column('response_status', sa.Integer(), nullable=False), sa.Column('response_body', postgresql.JSON(astext_type=sa.Text()), nullable=True), sa.Column('execution_time_ms', sa.Integer(), nullable=False), sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True), sa.ForeignKeyConstraint(['user_id'], ['users.id'], ), sa.PrimaryKeyConstraint('id'))
    op.create_index(op.f('ix_api_logs_created_at'), 'api_logs', ['created_at'], unique=False)
    op.create_index(op.f('ix_api_logs_endpoint'), 'api_logs', ['endpoint'], unique=False)
    op.create_index(op.f('ix_api_logs_user_id'), 'api_logs', ['user_id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_api_logs_user_id'), table_name='api_logs')
    op.drop_index(op.f('ix_api_logs_endpoint'), table_name='api_logs')
    op.drop_index(op.f('ix_api_logs_created_at'), table_name='api_logs')
    op.drop_table('api_logs')
    op.drop_index(op.f('ix_structured_data_user_id'), table_name='structured_data')
    op.drop_index(op.f('ix_structured_data_data_type'), table_name='structured_data')
    op.drop_index(op.f('ix_structured_data_created_at'), table_name='structured_data')
    op.drop_table('structured_data')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
