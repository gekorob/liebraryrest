import json

from liebraryrest.models import Booking, Loan
from ..factories import UserFactory, BookFactory


def test_list_users(client, db):
    UserFactory.create_batch(3)
    db.session.commit()

    res = client.get('/api/users')

    assert res.status_code == 200
    assert len(json.loads(res.data.decode('UTF-8'))) == 3


def test_show_user(client, user):
    res = client.get('/api/users/{}'.format(user.id))

    user_found = json.loads(res.data.decode('UTF-8'))

    assert user_found['nickname'] == user.nickname


def test_get_bookings_for_a_specified_user(client, user, book, db):
    Booking(book, user).save()
    new_book = BookFactory()
    new_user = UserFactory()
    Booking(new_book, new_user).save()
    Booking(new_book, user).save()
    db.session.commit()

    res = client.get('/api/users/{}/bookings'.format(user.id))

    bookings = json.loads(res.data.decode('UTF-8'))
    assert len(bookings) == 2


def test_get_loans_for_a_specified_user(client, user, book, db):
    Booking(book, user).save()
    Booking(BookFactory(), user).save()
    Booking(BookFactory(), user).save()
    Booking(BookFactory(), UserFactory()).save()
    db.session.commit()

    for b in Booking.query.filter(Booking.user_id == user.id).all():
        Loan(b).save()
    db.session.commit()

    res = client.get('/api/users/{}/loans'.format(user.id))

    loans = json.loads(res.data.decode('UTF-8'))
    assert len(loans) == 3
