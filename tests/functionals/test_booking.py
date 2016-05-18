from liebraryrest.models import Book, Booking
from ..factories import BookFactory, UserFactory


def test_booking_on_zero_remaining_book(client, db):
    user = UserFactory(nickname='gekorob')
    book = BookFactory(title='James e la pesca gigante', quantity=0)
    db.session.commit()

    res = client.post('/api/books/{}/booking/{}'.format(book.isbn, user.id))

    assert res.status_code == 400
    assert Book.get_by_isbn(book.isbn).quantity == 0


def test_booking_on_quantity_book(client, db):
    user = UserFactory(nickname='gekorob')
    book = BookFactory(title='James e la pesca gigante', quantity=1)
    db.session.commit()

    res = client.post('/api/books/{}/booking/{}'.format(book.isbn, user.id))

    assert res.status_code == 201
    assert Book.get_by_isbn(book.isbn).quantity == 0
    assert Booking.query.count() == 1

def test_booking_on_already_booked_book(client, db):
    user = UserFactory(nickname='gekorob')
    book = BookFactory(title='James e la pesca gigante', quantity=1)
    db.session.commit()

    Booking(book, user).save(True)

    res = client.post('/api/books/{}/booking/{}'.format(book.isbn, user.id))

    assert res.status_code == 400



