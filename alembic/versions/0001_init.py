from alembic import op
import sqlalchemy as sa

revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('api_key', sa.String(255), unique=True, nullable=False)
    )
    op.create_table('medias',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('content_type', sa.String(100), nullable=False),
        sa.Column('path', sa.String(500), nullable=False),
        sa.Column('author_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False)
    )
    op.create_table('tweets',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('author_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False)
    )
    op.create_table('tweet_media',
        sa.Column('tweet_id', sa.Integer, sa.ForeignKey('tweets.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('media_id', sa.Integer, sa.ForeignKey('medias.id', ondelete='CASCADE'), primary_key=True)
    )
    op.create_table('likes',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('tweet_id', sa.Integer, sa.ForeignKey('tweets.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False)
    )
    op.create_table('follows',
        sa.Column('follower_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('followee_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False)
    )

def downgrade():
    op.drop_table('follows')
    op.drop_table('likes')
    op.drop_table('tweet_media')
    op.drop_table('tweets')
    op.drop_table('medias')
    op.drop_table('users')
