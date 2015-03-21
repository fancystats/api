#!/usr/bin/env python

from flask.ext.script import Manager

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


if __name__ == "__main__":
    manager.run()
