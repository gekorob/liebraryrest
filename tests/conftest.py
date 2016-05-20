# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import pytest

from liebraryrest.app import create_app
from liebraryrest.database import db as _db
from liebraryrest.models import Booking
from liebraryrest.settings import TestConfig
from .factories import UserFactory, BookFactory


@pytest.yield_fixture(scope='function')
def app():
    """An application for the tests."""
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.yield_fixture(scope='function')
def db(app):
    """A database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()

@pytest.fixture()
def user(db):
    user = UserFactory(nickname='gekorob')
    db.session.commit()
    return user

@pytest.fixture()
def book(db):
    book = BookFactory(title='Lord of the Rings')
    db.session.commit()
    return book

@pytest.fixture()
def booking(book, user, db):
    booking = Booking(book, user)
    booking.save()
    db.session.commit()
    return booking
