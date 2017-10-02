from alembic import op
import sqlalchemy as sa



"""chat events chat id

Revision ID: bf33ede69739
Revises: 80d08655f15a
Create Date: 2017-10-02 05:40:53.239786

"""

# revision identifiers, used by Alembic.
revision = 'bf33ede69739'
down_revision = '80d08655f15a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chat_events', sa.Column('chat_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'chat_events', 'chats', ['chat_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'chat_events', type_='foreignkey')
    op.drop_column('chat_events', 'chat_id')
    # ### end Alembic commands ###
