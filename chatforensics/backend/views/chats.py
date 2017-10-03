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
    "messages": fields.Integer
})

chat_list_model = ns.model("ChatList", {
    "chats": fields.List(fields.Nested(chat_list_item_model))
})

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
                "messages": g.db.query(func.count("*")).select_from(Message).filter(Message.chat_id == chat.id).scalar()
            })

        return {
            "chats": all_chats,
        }


@ns.route("/<int:chat_id>")
class ChatInfoResource(ResourceBase):
    @ns.marshal_with(chat_list_model)
    def get(self):
        db_chats = g.db.query(Chat).order_by(Chat.id).all()

        all_chats = []
        for chat in db_chats:
            all_chats.append({
                "id": chat.id,
                "name": chat.friendly_name or chat.backend_uid,
                "messages": g.db.query(func.count("*")).select_from(Message).filter(Message.chat_id == chat.id).scalar()
            })

        return {
            "chats": all_chats,
        }
