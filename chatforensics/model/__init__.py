# This Python file uses the following encoding: utf-8
import os

from sqlalchemy import Column, Integer, String, create_engine, inspect, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relation
from sqlalchemy.schema import Index

from chatforensics.model.types import BackendType

debug = os.environ.get('DEBUG', False)

engine = create_engine(os.environ["DB_URL"], convert_unicode=True, pool_recycle=3600)

if debug:
    engine.echo = True

sm = sessionmaker(autocommit=False,
                  autoflush=False,
                  bind=engine)

base_session = scoped_session(sm)

Base = declarative_base()
Base.query = base_session.query_property()

class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    backend_type = Column(Enum(BackendType), nullable=False)
    backend_uid = Column(String, nullable=False)

    created_at = Column(DateTime)
    friendly_name = Column(String)
    topic = Column(String)

    extra_meta = Column(JSONB)


class ChatUser(Base):
    __tablename__ = 'chat_users'

    id = Column(Integer, primary_key=True)
    backend_type = Column(Enum(BackendType), nullable=False)
    backend_uid = Column(String, nullable=False)

    friendly_name = Column(String)

    extra_meta = Column(JSONB)


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    backend_uid = Column(String, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.id'))
    chat_user_id = Column(Integer, ForeignKey('chat_users.id'))

    created_at = Column(DateTime, nullable=False)
    edited_at = Column(DateTime)

    content = Column(String)
    raw_content = Column(String)

    extra_meta = Column(JSONB)


# Indexes

Index("index_message_created", Message.created_at)

# Relations

Message.chat = relation(Chat)
Message.chat_user = relation(ChatUser)
