import sys
import json
import operator

from sqlalchemy import func

from chatforensics.model import sm, ChatUser, Chat, Message
from chatforensics.chathandlers import ALL_HANDLERS

state = {
    "altered": 0
}


def insert_or_update(db, model_type, item, flush=False):
    if isinstance(item, list):
        for i in item.copy():
            in_db = db.query(func.count("*")).select_from(model_type).filter(model_type.backend_uid == i["backend_uid"]).scalar() != 0
            if in_db:
                item.remove(i)
    else:
        in_db = db.query(func.count("*")).select_from(model_type).filter(model_type.backend_uid == item.backend_uid).scalar() != 0

    print(in_db, state, type(item))

    if isinstance(item, list):
        db.bulk_insert_mappings(
            model_type,
            item
        )
        db.commit()
    elif not in_db:
        db.add(item)
        if flush:
            db.flush()
        state["altered"] += 1
    elif item.id:
        db.merge(item)
        state["altered"] += 1

    if state["altered"] > 512:
        state["altered"] = 0
        db.commit()


def import_file(db, filename: str):
    message_bulk = []

    for handler in ALL_HANDLERS:
        file_handler = handler(filename)
        if not file_handler.is_valid():
            print('not valid for ' + str(file_handler))
            continue

        for chat_user in file_handler.chat_users:
            insert_or_update(db, ChatUser, chat_user, True)
        db.commit()

        for chat in file_handler.chats:
            insert_or_update(db, Chat, chat, True)
        db.commit()

        for message in file_handler.messages:
            message_bulk.append(message)
            if len(message_bulk) > 1024:
                insert_or_update(db, Message, message_bulk)
                message_bulk = []
        
        # Flush out the message bulk if we still have unflushed messages.
        if message_bulk:
            insert_or_update(db, Message, message_bulk)
            message_bulk = []

    db.commit()


if __name__ == "__main__":
    db = sm()
    import_file(db, sys.argv[1])
