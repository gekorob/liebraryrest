# -*- coding: utf-8 -*-
import datetime
from factory import Sequence, Faker, SubFactory
from factory.alchemy import SQLAlchemyModelFactory

from liebraryrest.database import db
from liebraryrest.models import Author, Book, User


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):
    """User factory"""

    class Meta:
        """Factory configuration."""
        model = User

    nickname = Faker('user_name')


class AuthorFactory(BaseFactory):
    """Author factory."""

    class Meta:
        """Factory configuration."""
        model = Author
        inline_args = ('first_name', 'last_name')

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    birth_date = Sequence(lambda n: datetime.date(1975, 1, 1) + datetime.timedelta(days=n))


class BookFactory(BaseFactory):
    """Book factory."""

    class Meta:
        """Factory configuration."""
        model = Book

    isbn = Faker('ean13')
    title = Faker('sentence', nb_words=6, variable_nb_words=True)
    author = SubFactory(AuthorFactory)
    abstract = Faker('text', max_nb_chars=350)
    pages = Sequence(lambda n: n)
    publisher = Faker('word')
    quantity = Sequence(lambda n: 1 + n)
