from datetime import datetime
from liebraryrest.database import db, Model
from sqlalchemy import UniqueConstraint


class User(Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(50), nullable=False, index=True)
    bookings = db.relationship('Booking', backref='user', lazy="dynamic")

    def __init__(self, nickname):
        self.nickname = nickname

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(int(user_id))

    def serialize(self, includes=None):
        d = super().serialize()
        d.pop('bookings')
        return d


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
            d.pop('books')
        return d


class Book(Model):
    isbn = db.Column(db.String(13), primary_key=True)
    title = db.Column(db.Text, nullable=False, index=True)
    abstract = db.Column(db.Text, nullable=True)
    pages = db.Column(db.Integer, nullable=True)
    publisher = db.Column(db.String(250), nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    bookings = db.relationship('Booking', backref='book', lazy="dynamic")

    def __init__(self, isbn, title, author, abstract=None,
                 pages=None, publisher=None, quantity=1):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.abstract = abstract
        self.pages = pages
        self.publisher = publisher
        self.quantity = quantity

    @classmethod
    def get_by_isbn(cls, book_isbn):
        return cls.query.get(book_isbn)

    def serialize(self, includes=None):
        d = super().serialize()
        if (includes is not None) and 'author' in includes:
            d['author'] = Book.serialize_list(self.author)
        else:
            d.pop('author')
        d.pop('bookings')
        return d

    def is_available(self):
        return self.quantity > 0


class Booking(Model):
    __table_args__ = (UniqueConstraint('book_isbn', 'user_id', name='_book_isbn_user_id'),)

    id = db.Column(db.Integer, primary_key=True)
    book_isbn = db.Column(db.String(13), db.ForeignKey('book.isbn'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, book, user):
        self.book = book
        self.user = user
        self.created_at = datetime.now()

    @classmethod
    def get_by_isbn_and_user_id(cls, book_isbn, user_id):
        return cls.query.filter(Booking.book_isbn == book_isbn, Booking.user_id == user_id).first()