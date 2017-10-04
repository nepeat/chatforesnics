# coding=utf-8
from flask import g, request
from flask_restplus import Namespace, abort, fields

from sqlalchemy import func

from chatforensics.model import Chat, Message
from chatforensics.backend.views.base import ResourceBase

ns = Namespace("chats", "Chat info/messages")

chat_list_item_model = ns.model("ChatListItem", {
    "id": fields.String,
    "name": fields.String,
    "created": fields.DateTime,
    "messages": fields.Integer
})

chat_list_model = ns.model("ChatList", {
    "chats": fields.List(fields.Nested(chat_list_item_model))
})

message_item_model = ns.model("Message", {
    "from": fields.Integer,
    "content": fields.String,
    "created": fields.DateTime,
    "extra_meta": fields.Raw
})

message_list_model = ns.model("MessageList", {
    "messages": fields.List(fields.Nested(message_item_model))
})

def get_chat_message_count(chat_id):
    return g.db.query(func.count("*")).select_from(Message).filter(Message.chat_id == chat_id).scalar()

@ns.route("/")
class ChatListResource(ResourceBase):
    @ns.marshal_with(chat_list_model)
    def get(self):
        db_chats = g.db.query(Chat).order_by(Chat.id).all()

        all_chats = []
        for chat in db_chats:
            all_chats.append({
                "id": chat.id,
                "name": chat.friendly_name or chat.backend_uid,
                "created": chat.created_at,
                "messages": get_chat_message_count(chat.id)
            })

        return {
            "chats": all_chats,
        }


@ns.route("/<int:chat_id>")
class ChatInfoResource(ResourceBase):
    @ns.marshal_with(message_list_model)
    def get(self, chat_id):
        db_messages = g.db.query(Message).filter(Message.chat_id == chat_id).limit(500).all()

        fmt_messages = []
        for message in db_messages:
            fmt_messages.append({
                "from": message.chat_user_id,
                "content": message.content,
                "created": message.created_at,
                "extra_meta": message.extra_meta
            })

        return {
            "messages": fmt_messages
        }
