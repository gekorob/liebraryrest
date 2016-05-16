from ..factories import BookFactory, UserFactory


def test_booking_on_zero_remaining_book(client, db):
    user = UserFactory(nickname='gekorob')
    book = BookFactory(title='James e la pesca gigante', available=0)
    db.session.commit()

    res = client.post('/api/books/{}/booking/{}'.format(book.isbn, user.id))

    assert res.status_code == 400
