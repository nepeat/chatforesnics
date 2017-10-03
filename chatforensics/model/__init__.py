# This Python file uses the following encoding: utf-8
import os

from sqlalchemy import Column, Integer, String, create_engine, inspect, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relation
from sqlalchemy.schema import Index

from chatforensics.model.types import BackendType, ChatEventType

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


class ChatEvent(Base):
    __tablename__ = 'chat_events'

    id = Column(Integer, primary_key=True)
    backend_type = Column(Enum(BackendType), nullable=False)
    backend_uid = Column(String, nullable=False)
    chat_id = Column(Integer, ForeignKey('chats.id'))

    created_at = Column(DateTime, nullable=False)

    event_type = Column(Enum(ChatEventType))
    event_meta = Column(JSONB)


class ChatUser(Base):
    __tablename__ = 'chat_users'

    id = Column(Integer, primary_key=True)
    backend_type = Column(Enum(BackendType), nullable=False)
    backend_uid = Column(String, nullable=False)

    friendly_name = Column(String)

    extra_meta = Column(JSONB)


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    backend_type = Column(Enum(BackendType), nullable=False)
    backend_uid = Column(String)
    chat_id = Column(Integer, ForeignKey('chats.id'))
    chat_user_id = Column(Integer, ForeignKey('chat_users.id'))

    created_at = Column(DateTime, nullable=False)
    edited_at = Column(DateTime)

    content = Column(String)
    raw_content = Column(String)

    extra_meta = Column(JSONB)


# Indexes

Index("index_unique_chat_uid", Chat.backend_uid, unique=True)
Index("index_unique_chat_event_uid", ChatEvent.backend_uid, unique=True)
Index("index_unique_chat_user_uid", ChatUser.backend_uid, unique=True)
Index("index_unique_message_uid", Message.backend_uid, unique=True)

Index("index_chat_event_uid", ChatEvent.backend_uid)
Index("index_chat_event_created", ChatEvent.created_at)

Index("index_message_chat_id", Message.chat_id)
Index("index_message_chat_user_id", Message.chat_user_id)
Index("index_message_created", Message.created_at)

# Relations

Message.chat = relation(Chat)
Message.chat_user = relation(ChatUser)

ChatEvent.chat = relation(Chat)
