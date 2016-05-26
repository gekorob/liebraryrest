from liebraryrest.models import Author
from liebrary import models as do


class AuthorRepository:
    def list(self, filter_params=None):
        qry = Author.query

        if filter_params is not None:
            qry = qry.filter(Author.name.contains(filter_params['name']))

        authors = [do.Author(a.id, a.name, a.birth_date) for a in qry.all()]

        return authors
