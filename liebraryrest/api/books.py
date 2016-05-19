import json
from flask import Blueprint, Response
from liebraryrest.models import Book, User, Booking

blueprint = Blueprint('books', __name__, url_prefix='/api/books')


@blueprint.route('')
def book_list():
    return Response(json.dumps(Book.serialize_list(Book.query.all())),
                    mimetype='application/json',
                    status=200)


@blueprint.route('/<int:book_isbn>')
def book_show(book_isbn):
    book = Book.get_by_isbn(book_isbn)

    if book is not None:
        return Response(book.to_json(),
                        mimetype='application/json',
                        status=200)

    return Response(json.dumps("No book found with isbn {}".format(book_isbn)),
                    mimetype='application/json',
                    status=404)


@blueprint.route('/<int:book_isbn>/booking/<int:user_id>', methods=['POST'])
def booking_on_a_book(book_isbn, user_id):
    book = Book.get_by_isbn(book_isbn)
    user = User.get_by_id(user_id)

    print('###' + book.isbn)
    print('###' + str(user.id))

    if (book is not None) and (user is not None):
        booking = Booking.get_by_isbn_and_user_id(book.isbn, user.id)
        if booking is not None:
            return Response(
                json.dumps("This book {} is already on the booking list of user {}"
                           .format(book.isbn, user.id)),
                mimetype='application/json',
                status=400
            )
        if book.is_available():
            book.quantity -= 1
            book.save()
            booking = Booking(book, user)
            booking.save()
            return Response(json.dumps(booking.to_json()),
                            mimetype='application/json',
                            status=201)
        return Response(json.dumps("Book {} is not available for booking".format(book_isbn, user_id)),
                        mimetype='application/json',
                        status=400)

    return Response(json.dumps("Unable to find Book: {} or user: {}".format(book_isbn, user_id)),
                    mimetype='application/json',
                    status=404)
