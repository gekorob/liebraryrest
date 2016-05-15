import json
from flask import Blueprint, Response
from liebraryrest.models import Book

blueprint = Blueprint('books', __name__, url_prefix='/api/books')


@blueprint.route('')
def book_list():
    return Response(json.dumps(Book.serialize_list(Book.query.all())),
                    mimetype='application/json',
                    status=200)


@blueprint.route('/<int:book_isbn>')
def author_show(book_isbn):
    book = Book.get_by_isbn(book_isbn)

    if book is not None:
        return Response(book.to_json(),
                        mimetype='application/json',
                        status=200)

    return Response(json.dumps("No book found with isbn {}".format(book_isbn)),
                    mimetype='application/json',
                    status=404)
