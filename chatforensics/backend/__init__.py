from flask import Flask, g

from chatforensics.model import sm
from chatforensics.backend.api import blueprint as api_blueprint

app = Flask(__name__)

@app.before_request
def before_request():
    g.db = sm()

@app.teardown_request
def teardown_request(_):
    if hasattr(g, "db"):
        g.db.close()
        del g.db

    if hasattr(g, "redis"):
        del g.redis

    return _


app.register_blueprint(api_blueprint, url_prefix="/api")
