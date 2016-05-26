from liebraryrest.models import Author
from liebrary import models as do


class AuthorRepository:
    def list(self):
        authors = [do.Author(a.id, a.name, a.birth_date) for a in Author.query.all()]

        return authors
