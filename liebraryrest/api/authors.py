import json

from flask import Blueprint, Response, request
from liebraryrest.models import Author, Book

blueprint = Blueprint('authors', __name__, url_prefix='/api/authors')


@blueprint.route('')
def author_list():
    qry = Author.query

    if request.args.get('name'):
        qry = qry.filter(Author.name.contains(request.args.get('name')))

    return Response(Author.list_to_json(qry.all()),
                    mimetype='application/json',
                    status=200)


@blueprint.route('/<int:author_id>')
def author_show(author_id):
    auth = Author.get_by_id(author_id)

    if auth is not None:
        return Response(auth.to_json(includes=['books']),
                        mimetype='application/json',
                        status=200)

    return Response(json.dumps("No author found with id {}".format(author_id)),
                    mimetype='application/json',
                    status=404)


@blueprint.route('/<int:author_id>/books')
def books_by_author(author_id):
    auth = Author.get_by_id(author_id)

    if auth is not None:
        return Response(Book.list_to_json(auth.books.all()),
                        mimetype='application/json',
                        status=200)

    return Response(json.dumps("No author found with id {}".format(author_id)),
                    mimetype='application/json',
                    status=404)
