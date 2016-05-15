import json
from ..factories import AuthorFactory, BookFactory


def test_list_empty_authors(client, db):
    res = client.get('/api/authors')

    assert res.status_code == 200
    assert res.data.decode('UTF-8') == json.dumps([])


def test_list_authors(client, db):
    authors = AuthorFactory.create_batch(3)

    res = client.get('/api/authors')

    assert res.status_code == 200
    assert json.loads(res.data.decode('UTF-8')) == [m.serialize() for m in authors]


def test_show_author_details_with_books(client, db):
    author = AuthorFactory(first_name='Mario', last_name='Rossi')
    books = BookFactory.create_batch(3, author=author)
    AuthorFactory.create_batch(3)
    db.session.commit()

    res = client.get('api/authors/{}'.format(author.id))
    author_found = json.loads(res.data.decode('UTF-8'))

    assert res.status_code == 200
    assert author_found['name'] == author.name
    assert len(author_found['books']) == 3



