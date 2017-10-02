import sys
import json
import operator

from chatforensics.model import sm, ChatUser, Chat, Message
from chatforensics.chathandlers import ALL_HANDLERS

state = {
    "altered": 0
}

def insert_or_update(db, model_type, item):
    db_item = db.query(model_type).filter(model_type.backend_uid == item.backend_uid).scalar()

    if not db_item:
        db.add(item)
        db.flush()
        state["altered"] += 1

    if db_item and item.id:
        db.merge(item)
        state["altered"] += 1

    if state["altered"] > 120:
        state["altered"] = 0
        db.commit()

def import_file(db, filename: str):
    for handler in ALL_HANDLERS:
        file_handler = handler(filename)
        if not file_handler.is_valid():
            print('not valid for ' + str(file_handler))
            continue

        for chat_user in file_handler.chat_users:
            insert_or_update(db, ChatUser, chat_user)

        for chat in file_handler.chats:
            insert_or_update(db, Chat, chat)

        for message in file_handler.messages:
            print(message.__dict__)
            insert_or_update(db, Message, message)

    db.commit()

if __name__ == "__main__":
    db = sm()
    import_file(db, sys.argv[1])
