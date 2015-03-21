from flask_peewee.db import Database

from nhlstats.models import db_proxy

from .app import app

db = Database(app)

db_proxy.initialize(db.database)
