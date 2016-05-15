from liebraryrest.database import db, Model


class Author(Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, index=True)
    birth_date = db.Column(db.DateTime, nullable=False)
    books = db.relationship('Book', backref='author', lazy="dynamic")

    def __init__(self, first_name, last_name, birth_date):
        self.name = "{0} {1}".format(first_name, last_name)
        self.birth_date = birth_date

    @classmethod
    def get_by_id(cls, author_id):
        return cls.query.get(int(author_id))

    def serialize(self, includes=None):
        d = super().serialize()
        d['birth_date'] = d['birth_date'].isoformat()
        if (includes is not None) and 'books' in includes:
            d['books'] = Book.serialize_list(self.books.all())
        else:
            del d['books']
        return d


class Book(Model):
    isbn = db.Column(db.String(13), primary_key=True)
    title = db.Column(db.Text, nullable=False, index=True)
    abstract = db.Column(db.Text, nullable=True)
    pages = db.Column(db.Integer, nullable=True)
    publisher = db.Column(db.String(250), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    def __init__(self, isbn, title, author, abstract=None, pages=None, publisher=None):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.abstract = abstract
        self.pages = pages
        self.publisher = publisher

    @classmethod
    def get_by_isbn(cls, book_isbn):
        return cls.query.get(book_isbn)

    def serialize(self, includes=None):
        d = super().serialize()
        if (includes is not None) and 'author' in includes:
            d['author'] = Book.serialize_list(self.author)
        else:
            del d['author']
        return d
