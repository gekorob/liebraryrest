from liebrary import models as do
from liebraryrest.repositories.author_repository import AuthorRepository
from ..factories import AuthorFactory


def test_list_empty_authors(db):
    repo = AuthorRepository()

    assert repo.list() == []


def test_list_authors(db):
    author_list = AuthorFactory.create_batch(3)
    repo = AuthorRepository()

    expected_authors = [do.Author(a.id, a.name, a.birth_date) for a in author_list]

    assert repo.list() == expected_authors


def test_list_authors_using_filter_on_name(db):
    AuthorFactory.create_batch(3)
    auth = AuthorFactory(first_name='Asimov')
    repo = AuthorRepository()

    expected_authors = [do.Author(auth.id, auth.name, auth.birth_date)]

    assert repo.list({'name': 'Asimov'}) == expected_authors
