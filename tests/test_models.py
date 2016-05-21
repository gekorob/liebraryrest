import pytest
from .factories import AuthorFactory, BookFactory, UserFactory

from liebraryrest.models import Author, User, Booking, Loan


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


def test_get_author_by_id(db):
    auth = AuthorFactory(first_name='Mario', last_name='Rossi')
    BookFactory.create_batch(10, author=auth)
    AuthorFactory.create_batch(24)
    db.session.commit()

    assert Author.query.count() == 25

    found_author = Author.get_by_id(auth.id)

    assert found_author.name == 'Mario Rossi'
    assert found_author.books.count() == 10


def test_get_author_by_id_with_not_existing_author(db):
    AuthorFactory.create_batch(24)

    assert Author.query.count() == 24
    assert Author.get_by_id(0) is None


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


def test_create_booking_on_existing_book(db):
    book = BookFactory()
    user = UserFactory()
    db.session.commit()

    booking = Booking(book, user)
    booking.save()

    assert booking.book_isbn == book.isbn
    assert booking.user_id == user.id
    assert len(book.bookings.all()) == 1
    assert len(user.bookings.all()) == 1


def test_no_double_booking(db):
    book = BookFactory()
    user = UserFactory()
    db.session.commit()

    booking = Booking(book, user)
    booking.save(True)

    with pytest.raises(Exception):
        Booking(book, user).save(True)


def test_get_booking_by_isbn_and_userid(db):
    book = BookFactory()
    user = UserFactory()
    db.session.commit()

    booking = Booking(book, user)
    booking.save(True)

    booking_found = Booking.get_by_isbn_and_user_id(book.isbn, user.id)

    assert booking_found == booking


def test_get_not_existing_booking_by_isbn_userid(db):
    booking_found = Booking.get_by_isbn_and_user_id('abcdefghilmno', 0)

    assert booking_found is None


def test_create_loan_from_a_booking(booking, db):
    loan = Loan(booking)
    loan.save()

    assert loan.book_isbn == booking.book_isbn
    assert loan.user_id == booking.user_id
    assert loan.booking == booking


def test_get_loan_by_booking_id(booking):
    Loan(booking).save(True)

    loan = Loan.get_by_booking_id(booking.id)

    assert loan.book_isbn == booking.book_isbn


def test_get_loan_by_isbn_and_userid(booking):
    Loan(booking).save(True)

    loan = Loan.get_by_isbn_and_user_id(booking.book_isbn, booking.user_id)

    assert loan.booking_id == booking.id
    assert loan.book_isbn == booking.book_isbn
    assert loan.user_id == booking.user_id
