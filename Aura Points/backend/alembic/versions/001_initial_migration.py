"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('wallet_address', sa.String(length=42), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_admin', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_wallet_address'), 'users', ['wallet_address'], unique=True)

    # Create personalities table
    op.create_table(
        'personalities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('twitter_handle', sa.String(length=100), nullable=True),
        sa.Column('youtube_channel_id', sa.String(length=100), nullable=True),
        sa.Column('image_url', sa.String(length=500), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_personalities_id'), 'personalities', ['id'], unique=False)
    op.create_index(op.f('ix_personalities_name'), 'personalities', ['name'], unique=False)
    op.create_index('idx_personality_slug', 'personalities', ['slug'], unique=False)
    op.create_index(op.f('ix_personalities_slug'), 'personalities', ['slug'], unique=True)

    # Create aura_scores table
    op.create_table(
        'aura_scores',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('personality_id', sa.Integer(), nullable=False),
        sa.Column('current_score', sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column('momentum_score', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('price_per_share', sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column('total_shares', sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column('volume_24h', sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['personality_id'], ['personalities.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('personality_id')
    )
    op.create_index('idx_aura_score_personality', 'aura_scores', ['personality_id'], unique=False)
    op.create_index('idx_aura_score_updated', 'aura_scores', ['updated_at'], unique=False)
    op.create_index(op.f('ix_aura_scores_id'), 'aura_scores', ['id'], unique=False)

    # Create aura_score_history table
    op.create_table(
        'aura_score_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('personality_id', sa.Integer(), nullable=False),
        sa.Column('score', sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column('momentum_score', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('price_per_share', sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column('volume_24h', sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['personality_id'], ['personalities.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_history_personality_timestamp', 'aura_score_history', ['personality_id', 'timestamp'], unique=False)
    op.create_index(op.f('ix_aura_score_history_id'), 'aura_score_history', ['id'], unique=False)
    op.create_index(op.f('ix_aura_score_history_timestamp'), 'aura_score_history', ['timestamp'], unique=False)

    # Create trades table
    op.create_table(
        'trades',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('personality_id', sa.Integer(), nullable=False),
        sa.Column('trade_type', sa.String(length=10), nullable=False),
        sa.Column('shares', sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column('price_per_share', sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column('total_cost', sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column('transaction_hash', sa.String(length=66), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['personality_id'], ['personalities.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('transaction_hash')
    )
    op.create_index('idx_trade_created', 'trades', ['created_at'], unique=False)
    op.create_index('idx_trade_personality', 'trades', ['personality_id'], unique=False)
    op.create_index('idx_trade_user', 'trades', ['user_id'], unique=False)
    op.create_index(op.f('ix_trades_id'), 'trades', ['id'], unique=False)

    # Create parlays table
    op.create_table(
        'parlays',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('legs', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('total_stake', sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column('potential_payout', sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('contract_address', sa.String(length=42), nullable=True),
        sa.Column('transaction_hash', sa.String(length=66), nullable=True),
        sa.Column('resolution_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_parlay_status', 'parlays', ['status'], unique=False)
    op.create_index('idx_parlay_user', 'parlays', ['user_id'], unique=False)
    op.create_index(op.f('ix_parlays_id'), 'parlays', ['id'], unique=False)

    # Create ml_signals_raw table
    op.create_table(
        'ml_signals_raw',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('personality_id', sa.Integer(), nullable=False),
        sa.Column('source', sa.String(length=50), nullable=False),
        sa.Column('raw_data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('processed_features', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('sentiment_score', sa.Numeric(precision=5, scale=4), nullable=True),
        sa.Column('engagement_delta', sa.Numeric(precision=20, scale=8), nullable=True),
        sa.Column('volume_velocity', sa.Numeric(precision=20, scale=8), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['personality_id'], ['personalities.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_ml_signal_personality', 'ml_signals_raw', ['personality_id'], unique=False)
    op.create_index('idx_ml_signal_source', 'ml_signals_raw', ['source'], unique=False)
    op.create_index('idx_ml_signal_timestamp', 'ml_signals_raw', ['timestamp'], unique=False)
    op.create_index(op.f('ix_ml_signals_raw_id'), 'ml_signals_raw', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_ml_signals_raw_id'), table_name='ml_signals_raw')
    op.drop_index('idx_ml_signal_timestamp', table_name='ml_signals_raw')
    op.drop_index('idx_ml_signal_source', table_name='ml_signals_raw')
    op.drop_index('idx_ml_signal_personality', table_name='ml_signals_raw')
    op.drop_table('ml_signals_raw')
    op.drop_index(op.f('ix_parlays_id'), table_name='parlays')
    op.drop_index('idx_parlay_user', table_name='parlays')
    op.drop_index('idx_parlay_status', table_name='parlays')
    op.drop_table('parlays')
    op.drop_index(op.f('ix_trades_id'), table_name='trades')
    op.drop_index('idx_trade_user', table_name='trades')
    op.drop_index('idx_trade_personality', table_name='trades')
    op.drop_index('idx_trade_created', table_name='trades')
    op.drop_table('trades')
    op.drop_index(op.f('ix_aura_score_history_timestamp'), table_name='aura_score_history')
    op.drop_index(op.f('ix_aura_score_history_id'), table_name='aura_score_history')
    op.drop_index('idx_history_personality_timestamp', table_name='aura_score_history')
    op.drop_table('aura_score_history')
    op.drop_index(op.f('ix_aura_scores_id'), table_name='aura_scores')
    op.drop_index('idx_aura_score_updated', table_name='aura_scores')
    op.drop_index('idx_aura_score_personality', table_name='aura_scores')
    op.drop_table('aura_scores')
    op.drop_index(op.f('ix_personalities_slug'), table_name='personalities')
    op.drop_index('idx_personality_slug', table_name='personalities')
    op.drop_index(op.f('ix_personalities_name'), table_name='personalities')
    op.drop_index(op.f('ix_personalities_id'), table_name='personalities')
    op.drop_table('personalities')
    op.drop_index(op.f('ix_users_wallet_address'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')

