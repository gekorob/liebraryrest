from liebraryrest.models import Author, User

from .factories import AuthorFactory, BookFactory, UserFactory


def test_create_user(db):
    user = UserFactory(nickname='gekorob')
    db.session.commit()

    assert user.id is not None
    assert user.nickname == 'gekorob'


def test_get_user_by_id(db):
    user = UserFactory(nickname='gekorob')
    db.session.commit()

    user_found = User.get_by_id(user.id)

    assert user_found.id == user.id
    assert user_found.nickname == user.nickname


def test_create_author(db):
    auth = AuthorFactory(first_name='Roby')
    db.session.commit()

    assert auth.id is not None
    assert auth.name.startswith('Roby')


def test_build_author_and_model_save(db):
    auth = AuthorFactory.build()
    auth.save()

    assert auth.id is not None


def test_create_book(db):
    auth = AuthorFactory(first_name='Mario', last_name='Rossi')
    book = BookFactory(title='History of Mario Rossi', author=auth)
    db.session.commit()

    assert auth.id is not None
    assert auth.name == 'Mario Rossi'
    assert book.isbn is not None
    assert book.title == 'History of Mario Rossi'
    assert book.author is not None
    assert auth.books.first() == book
    assert book.author == auth


def test_build_book_and_model_save(db):
    auth = AuthorFactory.build()
    book = BookFactory.build(author=auth)
    book.save()

    assert auth.id is not None
    assert book.isbn is not None
    assert auth.books.first() == book
    assert book.author == auth


def test_get_author_by_id(db):
    auth = AuthorFactory(first_name='Mario', last_name='Rossi')
    BookFactory.create_batch(10, author=auth)
    AuthorFactory.create_batch(24)
    db.session.commit()

    assert Author.query.count() == 25

    found_author = Author.get_by_id(auth.id)

    assert found_author.name == 'Mario Rossi'
    assert found_author.books.count() == 10


def test_cannot_find_author(db):
    AuthorFactory.create_batch(24)

    assert Author.query.count() == 24
    assert Author.get_by_id(0) is None
