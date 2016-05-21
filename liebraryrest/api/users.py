import json

from flask import Blueprint, Response, request
from liebraryrest.models import User, Booking, Loan

blueprint = Blueprint('users', __name__, url_prefix='/api/users')


@blueprint.route('')
def user_list():
    return Response(User.list_to_json(User.query.all()),
                    mimetype='application/json',
                    status=200)


@blueprint.route('/<int:user_id>')
def author_show(user_id):
    users = User.get_by_id(user_id)

    if users is not None:
        return Response(users.to_json(includes=['books']),
                        mimetype='application/json',
                        status=200)

    return Response(json.dumps("No author found with id {}".format(user_id)),
                    mimetype='application/json',
                    status=404)


@blueprint.route('/<int:user_id>/bookings')
def user_bookings(user_id):
    user = User.get_by_id(user_id)

    if user is not None:
        return Response(Booking.list_to_json(user.bookings.all()),
                        mimetype='application/json',
                        status=200)

    return Response(json.dumps("No author found with id {}".format(user_id)),
                    mimetype='application/json',
                    status=404)


@blueprint.route('/<int:user_id>/loans')
def user_loans(user_id):
    user = User.get_by_id(user_id)

    if user is not None:
        return Response(Loan.list_to_json(user.loans.all()),
                        mimetype='application/json',
                        status=200)

    return Response(json.dumps("No author found with id {}".format(user_id)),
                    mimetype='application/json',
                    status=404)
