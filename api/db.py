"""

Database
=========

Borrowed from flask-peewee, this is a heavily modified version of the Database
class that adds support for peewee.Proxy and disables database session closing
during testing as that wipes the in-memory SQLite database.

"""

import sys
import os

import peewee
from playhouse.db_url import connect

from nhlstats.models import db_proxy

from api.app import app


def load_class(s):
    path, klass = s.rsplit('.', 1)
    __import__(path)
    mod = sys.modules[path]
    return getattr(mod, klass)


class ImproperlyConfigured(Exception):
    pass


class Database(object):
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.load_database()
        self.register_handlers()

    def load_database(self):
        if 'DATABASE_URL' in os.environ:
            self.database = connect(os.environ['DATABASE_URL'])
        else:
            self.database = self.load_database_from_config()
        db_proxy.initialize(self.database)

    def load_database_from_config(self):
        self.database_config = dict(self.app.config['DATABASE'])
        try:
            self.database_name = self.database_config.pop('name')
            self.database_engine = self.database_config.pop('engine')
        except KeyError:
            raise ImproperlyConfigured(
                'Please specify a "name" and "engine" for your database')

        try:
            self.database_class = load_class(self.database_engine)
            assert issubclass(self.database_class, peewee.Database)
        except ImportError:
            raise ImproperlyConfigured('Unable to import: "%s"' %
                                       self.database_engine)
        except AttributeError:
            raise ImproperlyConfigured('Database engine not found: "%s"' %
                                       self.database_engine)
        except AssertionError:
            raise ImproperlyConfigured(
                'Engine not subclass of peewee.Database: "%s"' %
                self.database_engine)

        return self.database_class(self.database_name, **self.database_config)

    def connect_db(self):
        if not self.app.TESTING:
            self.database.connect()

    def close_db(self, exc):
        if not self.database.is_closed() and not self.app.TESTING:
            self.database.close()

    def register_handlers(self):
        self.app.before_request(self.connect_db)
        self.app.teardown_request(self.close_db)


db = Database(app)
