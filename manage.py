#!/usr/bin/env python

from flask.ext.script import Manager

from nhlstats import fixtures
from nhlstats.db import create_tables, drop_tables

from api.app import create_app

app = create_app()
manager = Manager(app)


@manager.command
def syncdb():
    """Create database tables if they don't exist"""
    create_tables()


@manager.command
def dropdb():
    """Drop tables if they do exist"""
    drop_tables()


def dumpdb():
    """Dump database data into fixtures"""
    fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
    fixtures.dump(basedir=fixtures_dir)


def loaddb():
    """Load data from fixtures into database"""
    fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
    fixtures.load(basedir=fixtures_dir)


if __name__ == "__main__":
    manager.run()
