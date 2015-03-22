from flask import Flask
from flask_peewee.db import Database

from nhlstats.models import db_proxy

app = db = None


def create_app():
    """A factory for creating flask apps."""
    global app, db

    app = Flask(__name__)
    app.config.from_object('api.config.Config')
    app.config.from_envvar('FANCYSTATS_SETTINGS', silent=True)

    db = Database(app)
    db_proxy.initialize(db.database)

    import api.resources

    return app
