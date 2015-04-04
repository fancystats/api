#!/usr/bin/env python

import logging
import os

from flask.ext.script import Manager

from nhlstats import fixtures
from nhlstats.db import create_tables, drop_tables

from api.app import create_app

logger = logging.getLogger('nhlstats')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

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


@manager.command
def dumpdb(dir=None):
    """Dump database data into fixtures"""
    if not dir:
        dir = os.path.join(os.path.dirname(__file__), 'fixtures')
    fixtures.dump(basedir=dir)


@manager.command
def loaddb():
    """Load data from fixtures into database"""
    if not dir:
        dir = os.path.join(os.path.dirname(__file__), 'fixtures')
    fixtures.load(basedir=dir)


if __name__ == "__main__":
    manager.run()
