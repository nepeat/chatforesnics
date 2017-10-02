import os
from typing import Iterable

from sqlalchemy import create_engine

from chatforensics.model import sm, ChatUser
from chatforensics.model.types import MessageData, ChatData


class HandlerBase:
    def __init__(self, filename: str):
        self.filename = filename
        self.db_app = sm()
        if not os.path.exists(filename):
            raise ValueError(f'File at `{filename}` does not exist.')

    def is_valid(self) -> bool:
        raise NotImplementedError

    # Messages

    def message_iter(self) -> Iterable[MessageData]:
        raise NotImplementedError

    @property
    def messages(self) -> Iterable[MessageData]:
        for message in self.message_iter():
            yield message

    # Chat users

    def chat_user_iter(self) -> Iterable[ChatUser]:
        raise NotImplementedError

    @property
    def chat_users(self) -> Iterable[ChatUser]:
        for chat in self.chat_user_iter():
            yield chat


    # Chats

    def chat_iter(self) -> Iterable[ChatData]:
        raise NotImplementedError

    @property
    def chats(self) -> Iterable[ChatData]:
        for chat in self.chat_iter():
            yield chat

    def __del__(self):
        self.db_app.close()
        del self.db_app

class SQLiteHandlerBase(HandlerBase): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = create_engine('sqlite:///' + os.path.abspath(self.filename))

    def __del__(self):
        super().__del__()
        if hasattr(self, 'db') and self.db:
            del self.db