import datetime

from chatforensics.chathandlers.base import SQLiteHandlerBase
from chatforensics.model import ChatUser, Chat, Message, ChatEvent
from chatforensics.model.types import MessageData, BackendType, ChatEventType


IMESSAGE_TABLES = [
    "message",
    "chat",
    "handle",
    "attachment"
]
HANDLE_QUERY = "SELECT * FROM handle;"
CHAT_QUERY = "SELECT * FROM chat;"
MESSAGE_QUERY = """
SELECT message.guid AS message_guid,
       message.text AS message_text,
       message.is_from_me AS message_is_from_me,
       message.date AS message_date,
       message.item_type AS message_item_type,
       message.group_title AS message_group_title,
       chat.guid AS chat_guid,
       handle.id AS handle_id
FROM chat
JOIN chat_message_join on chat.ROWID = chat_message_join.chat_id
JOIN message on message.ROWID = chat_message_join.message_id
JOIN handle on message.handle_id = handle.ROWID
ORDER BY message.date;
"""

class iMessageHandler(SQLiteHandlerBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.guid_cache = {}
        self.last_names = {}

    def _get_chat(self, guid):
        if guid not in self.guid_cache:
            result = self.db_app.query(Chat).filter(Chat.backend_uid == guid).scalar()
            if result:
                self.guid_cache[guid] = result

        return self.guid_cache.get(guid, None)

    def _get_chat_user(self, guid):
        if guid not in self.guid_cache:
            result = self.db_app.query(ChatUser).filter(ChatUser.backend_uid == guid).scalar()
            if result:
                self.guid_cache[guid] = result

        return self.guid_cache.get(guid, None)

    def is_valid(self):
        with self.db.connect() as db:
            tables = [x[0] for x in list(db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())]
            key_tables = [x for x in tables if x in IMESSAGE_TABLES]
            if len(key_tables) != len(IMESSAGE_TABLES):
                print(key_tables)
                print(IMESSAGE_TABLES)
                raise ValueError("Missing tables.")

        return True

    def chat_user_iter(self):
        with self.db.connect() as db:
            handle_query = db.execute(HANDLE_QUERY)
            for handle in handle_query:
                yield ChatUser(
                    backend_type=BackendType.imessage,
                    backend_uid=handle.id,
                    friendly_name=handle.id
                )

    def chat_iter(self):
        with self.db.connect() as db:
            handle_query = db.execute(CHAT_QUERY)
            for handle in handle_query:
                yield Chat(
                    backend_type=BackendType.imessage,
                    backend_uid=handle.guid,
                    friendly_name=handle.chat_identifier,
                )

    def message_iter(self):
        with self.db.connect() as db:
            message_query = db.execute(MESSAGE_QUERY)
            for message in message_query:
                # XXX iOS ?? suddenly made dates very very precise?
                if message["message_date"] > 5000000000:
                    message_created_at = datetime.datetime.utcfromtimestamp((int(message["message_date"]) / 1000000000) + 978307200)
                else:
                    message_created_at = datetime.datetime.utcfromtimestamp(int(message["message_date"]) + 978307200)

                # Group name change = 2
                if message["message_item_type"] == 2:
                    yield ChatEvent(
                        backend_uid=message["message_guid"],
                        backend_type=BackendType.imessage,
                        chat_id=self._get_chat(message["chat_guid"]).id,
                        created_at=message_created_at,
                        event_type=ChatEventType.group_name_change,
                        event_meta={
                            "before": self.last_names.get(message["chat_guid"], ""),
                            "after": message["message_group_title"]
                        }
                    )
                    self.last_names[message["chat_guid"]] = message["message_group_title"]
                    self._get_chat(message["chat_guid"]).friendly_name = message["message_group_title"]
                    self.db_app.commit()

                # Fill in the chat creation date if not filled in yet.
                if not self._get_chat(message["chat_guid"]).created_at:
                    self._get_chat(message["chat_guid"]).created_at = message_created_at
                    self.db_app.commit()

                if not message["message_text"]:
                    continue

                # XXX/HACK Add argument to choose between dict and heavy objects later.
                yield dict(
                    backend_type=BackendType.imessage,
                    backend_uid=message["message_guid"],
                    chat_id=self._get_chat(message["chat_guid"]).id,
                    chat_user_id=self._get_chat_user(message["handle_id"]).id,
                    created_at=message_created_at,
                    content=message["message_text"],
                    raw_content=message["message_text"],
                    extra_meta={
                        "from_me": message["message_is_from_me"] == 1
                    }
                )
