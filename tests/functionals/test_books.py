import json

from liebraryrest.models import Book
from ..factories import BookFactory, AuthorFactory


def test_list_empty_books(client, db):
    res = client.get('/api/books')

    assert res.status_code == 200
    assert res.data.decode('UTF-8') == json.dumps([])


def test_list_books(client, db):
    books = BookFactory.create_batch(3)

    res = client.get('/api/books')

    assert res.status_code == 200
    assert json.loads(res.data.decode('UTF-8')) == Book.serialize_list(books)


def test_show_book(client, book, db):
    BookFactory.create_batch(3)
    db.session.commit()
    
    res = client.get('api/books/{}'.format(book.isbn))
    assert res.status_code == 200

    book_found = json.loads(res.data.decode('UTF-8'))

    assert book_found['isbn'] == book.isbn
    assert book_found['title'] == book.title
    assert book_found['abstract'] == book.abstract
    assert book_found['pages'] == book.pages
    assert book_found['publisher'] == book.publisher
    assert book_found['author_id'] == book.author_id


def test_list_books_by_author_id(client, db):
    author = AuthorFactory(first_name='Mario', last_name='Rossi')
    BookFactory.create_batch(3, author=author)
    BookFactory.create_batch(5)
    db.session.commit()

    res = client.get('api/authors/{}/books'.format(author.id))
    assert res.status_code == 200

    books_found = json.loads(res.data.decode('UTF-8'))

    assert len(books_found) == 3


