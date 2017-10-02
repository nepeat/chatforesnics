from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

"""chat events

Revision ID: 80d08655f15a
Revises: 62dc90f35948
Create Date: 2017-10-02 05:09:05.067257

"""

# revision identifiers, used by Alembic.
revision = '80d08655f15a'
down_revision = '62dc90f35948'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat_events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('backend_type', postgresql.ENUM('imessage', 'discord', 'skype', name='backendtype', create_type=False), nullable=False),
    sa.Column('backend_uid', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('event_type', postgresql.ENUM('group_name_change', name='chateventtype'), nullable=True),
    sa.Column('event_meta', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('index_chat_event_created', 'chat_events', ['created_at'], unique=False)
    op.create_index('index_chat_event_uid', 'chat_events', ['backend_uid'], unique=False)
    op.create_index('index_unique_chat_event_uid', 'chat_events', ['backend_uid'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('index_unique_chat_event_uid', table_name='chat_events')
    op.drop_index('index_chat_event_uid', table_name='chat_events')
    op.drop_index('index_chat_event_created', table_name='chat_events')
    op.drop_table('chat_events')
    # ### end Alembic commands ###