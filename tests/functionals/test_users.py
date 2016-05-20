import json

from liebraryrest.models import Booking
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
    booking = Booking(book, user).save()
    new_book = BookFactory()
    new_user = UserFactory()
    Booking(new_book, new_user).save()
    Booking(new_book, user).save()
    db.session.commit()

    res = client.get('/api/users/{}/bookings'.format(user.id))

    bookings = json.loads(res.data.decode('UTF-8'))
    assert len(bookings) == 2
