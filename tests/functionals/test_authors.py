import json

from liebraryrest.models import Author, Book
from ..factories import AuthorFactory, BookFactory


def test_list_empty_authors(client, db):
    res = client.get('/api/authors')

    assert res.status_code == 200
    assert res.data.decode('UTF-8') == json.dumps([])


def test_list_authors(client, db):
    authors = AuthorFactory.create_batch(3)

    res = client.get('/api/authors')

    assert res.status_code == 200
    assert json.loads(res.data.decode('UTF-8')) == Author.serialize_list(authors)


def test_search_authors_by_name(client, db):
    AuthorFactory(first_name='Mario', last_name='Bianchi')
    AuthorFactory(first_name='Mario', last_name='Rossi')
    AuthorFactory(first_name='Nazario', last_name='Mossi')
    db.session.commit()

    res = client.get('/api/authors?name=Mario')
    assert len(json.loads(res.data.decode('UTF-8'))) == 2

    res = client.get('/api/authors?name=ario')
    assert len(json.loads(res.data.decode('UTF-8'))) == 3

    res = client.get('/api/authors?name=ossi')
    assert len(json.loads(res.data.decode('UTF-8'))) == 2

    res = client.get('/api/authors?name=mario%20rossi')
    assert len(json.loads(res.data.decode('UTF-8'))) == 1


def test_show_author_details_with_books(client, db):
    author = AuthorFactory(first_name='Mario', last_name='Rossi')
    books = BookFactory.create_batch(3, author=author)
    AuthorFactory.create_batch(3)
    db.session.commit()

    res = client.get('api/authors/{}'.format(author.id))
    author_found = json.loads(res.data.decode('UTF-8'))

    assert res.status_code == 200
    assert author_found['name'] == author.name
    assert author_found['birth_date'] == author.birth_date.isoformat()
    assert len(author_found['books']) == 3
    assert author_found['books'] == Book.serialize_list(books)
