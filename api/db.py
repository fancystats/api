from nhlstats.models import db_proxy

from .app import app
from api.database import Database

db = Database(app)
db_proxy.initialize(db.database)
