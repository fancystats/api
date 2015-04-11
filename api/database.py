import sys

import peewee

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
        self.database_config = dict(self.app.config['DATABASE'])
        try:
            self.database_name = self.database_config.pop('name')
            self.database_engine = self.database_config.pop('engine')
        except KeyError:
            raise ImproperlyConfigured(
                'Please specify a "name" and "engine" for your database'
            )

        try:
            self.database_class = load_class(self.database_engine)
            assert issubclass(self.database_class, peewee.Database)
        except ImportError:
            raise ImproperlyConfigured(
                'Unable to import: "%s"' % self.database_engine
            )
        except AttributeError:
            raise ImproperlyConfigured(
                'Database engine not found: "%s"' % self.database_engine
            )
        except AssertionError:
            raise ImproperlyConfigured(
                'Engine not subclass of peewee.Database: "%s"' %
                self.database_engine
            )

        self.database = self.database_class(
            self.database_name, **self.database_config)
        db_proxy.initialize(self.database)

    def connect_db(self):
        if not app.TESTING:
            self.database.connect()

    def close_db(self, exc):
        if not self.database.is_closed() and not app.TESTING:
            self.database.close()

    def register_handlers(self):
        self.app.before_request(self.connect_db)
        self.app.teardown_request(self.close_db)
