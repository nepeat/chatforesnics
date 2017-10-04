from flask import Flask, g, request

from chatforensics.model import sm
from chatforensics.backend.api import blueprint as api_blueprint

app = Flask(__name__)

@app.before_request
def before_request():
    g.db = sm()

@app.before_request
def debug_cors():
    if not app.debug:
        return

    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()

        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']

        h = resp.headers

        # Allow the origin which made the XHR
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        # Allow the actual method
        h['Access-Control-Allow-Methods'] = request.headers['Access-Control-Request-Method']

        # We also keep current headers
        if headers is not None:
            h['Access-Control-Allow-Headers'] = headers

        return resp

@app.after_request
def set_allow_origin(response=None):
    """ Set origin for GET, POST, PUT, DELETE requests """

    h = response.headers

    # Allow crossdomain for other HTTP Verbs
    if request.method != 'OPTIONS' and 'Origin' in request.headers:
        h['Access-Control-Allow-Origin'] = request.headers['Origin']


    return response

@app.teardown_request
def teardown_request(response=None):
    if hasattr(g, "db"):
        g.db.close()
        del g.db

    if hasattr(g, "redis"):
        del g.redis

    return response


app.register_blueprint(api_blueprint, url_prefix="/api")
