from flask import Blueprint

blueprint = Blueprint('books', __name__, url_prefix='/api/books')
