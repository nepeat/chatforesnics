from chatforensics.chathandlers._handlers import *  # NOQA

ALL_HANDLERS = [
    klass
    for name, klass in globals().items()
    if name.endswith("Handler")
]
