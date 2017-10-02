import enum

class BackendType(enum.Enum):
    imessage = 1
    discord = 2
    skype = 3


class ChatEventType(enum.Enum):
    group_name_change = 1


class MessageData:
    __slots__ = ["content", "raw_content", "created_at", "edited_at", "extra_meta"]

    def __repr__(self):
        return f"<MessageData>"

    def __str__(self):
        return f"{self.created_at} - {self.content}"

    def __init__(self, content, raw_content, created_at=None, edited_at=None, extra_meta=None):
        self.content = content
        self.raw_content = raw_content
        self.created_at = created_at
        self.edited_at = edited_at
        self.extra_meta = extra_meta or {}


class ChatData:
    __slots__ = ["content", "raw_content", "created_at", "edited_at", "extra_meta"]

    def __repr__(self):
        return f"<ChatData>"

    def __init__(self, content, raw_content, created_at=None, edited_at=None, extra_meta=None):
        self.content = content
        self.raw_content = raw_content
        self.created_at = created_at
        self.edited_at = edited_at
        self.extra_meta = extra_meta or {}
