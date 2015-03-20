from flask_peewee.db import Database
from nhlstats.db import create_tables, drop_tables

from .app import app

db = Database(app)
