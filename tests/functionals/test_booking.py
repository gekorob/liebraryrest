from time import sleep

from liebraryrest.models import Book, Booking
from ..factories import BookFactory, UserFactory


def test_booking_on_zero_remaining_book(client, user, book, db):
    book.quantity = 0
    book.save()
    db.session.commit()

    res = client.post('/api/books/{}/booking/{}'.format(book.isbn, user.id))

    assert res.status_code == 400
    assert Book.get_by_isbn(book.isbn).quantity == 0


def test_booking_on_quantity_book(client, user, book):
    previous_quantity = book.quantity
    res = client.post('/api/books/{}/booking/{}'.format(book.isbn, user.id))

    assert res.status_code == 201
    assert Book.get_by_isbn(book.isbn).quantity == (previous_quantity - 1)
    assert Booking.query.count() == 1


def test_booking_on_already_booked_book(client, user, book, db):
    Booking(book, user)
    db.session.commit()


    res = client.post('/api/books/{}/booking/{}'.format(book.isbn, user.id))

    assert res.status_code == 400
