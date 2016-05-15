import json


from flask import Blueprint, Response
from liebraryrest.models import Author

blueprint = Blueprint('authors', __name__, url_prefix='/api/authors')


@blueprint.route('')
def author_list():
    return Response(Author.list_to_json(Author.query.all()),
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
