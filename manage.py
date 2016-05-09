#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Management script."""
import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server, Shell
from flask_script.commands import Clean, ShowUrls

from liebraryrest.app import create_app
from liebraryrest.database import db
from liebraryrest.models import Book, Author
from liebraryrest.settings import DevConfig, ProdConfig

CONFIG = ProdConfig if os.environ.get('LIEBRARYREST_ENV') == 'prod' else DevConfig
HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

app = create_app(CONFIG)
manager = Manager(app)
migrate = Migrate(app, db)


def _make_context():
    """Return context dict for a shell session so you can access app, db, and models by default."""
    return {'app': app, 'db': db, 'Author': Author, 'Book': Book}


@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)
manager.add_command('urls', ShowUrls())
manager.add_command('clean', Clean())

if __name__ == '__main__':
    manager.run()
