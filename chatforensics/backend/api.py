from flask import Blueprint
from flask_restplus import Api

from chatforensics.backend.views import chats

blueprint = Blueprint("api", __name__)
api = Api(
    blueprint
)

@api.errorhandler
def default_error_handler(error):
    """Default error handler"""
    return {
        'message': str(error)
    }, getattr(error, 'code', 500)

api.add_namespace(chats.ns)
