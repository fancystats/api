#!/usr/bin/env python

from flask.ext.script import Manager

from api.app import app
from api.db import create_tables, drop_tables

manager = Manager(app)


@manager.command
def syncdb():
    create_tables()


@manager.command
def dropdb():
    drop_tables()


if __name__ == "__main__":
    manager.run()
