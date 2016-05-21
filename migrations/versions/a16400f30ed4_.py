"""empty message

Revision ID: a16400f30ed4
Revises: 922965edee4a
Create Date: 2016-05-21 13:57:00.526974

"""

# revision identifiers, used by Alembic.
revision = 'a16400f30ed4'
down_revision = '922965edee4a'

from alembic import op
import sqlalchemy as sa
import os
from datetime import datetime
from sqlalchemy.sql import table, column
from csv import DictReader

user_table = table('user',
                   column('id', sa.Integer),
                   column('nickname', sa.String))

author_table = table('author',
                     column('id', sa.Integer),
                     column('name', sa.String),
                     column('birth_date', sa.DateTime))

book_table = table('book',
                   column('isbn', sa.String),
                   column('title', sa.String),
                   column('author_id', sa.Integer),
                   column('quantity', sa.Integer))

migrations_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir)
csv_path = os.path.join(migrations_dir, 'csv')


def upgrade():
    users_file = os.path.join(csv_path, 'users.csv')
    authors_file = os.path.join(csv_path, 'authors.csv')
    books_file = os.path.join(csv_path, 'books.csv')

    _seed(user_table, users_file)
    _seed(author_table, authors_file,
          {'birth_date': (lambda d: datetime.strptime(d, '%Y%m%d'))})
    _seed(book_table, books_file)


def downgrade():
    _downgrade(user_table)
    _downgrade(author_table)
    _downgrade(book_table, 'isbn')


def _seed(table_obj, file_path, tx=None):
    with open(file_path, 'r') as f:
        reader = DictReader(f, delimiter=',')
        rows = list(reader)
    print(rows)

    if tx is not None:
        rows = [_tx_row(row, tx) for row in rows]

    op.bulk_insert(table_obj, rows)


def _tx_row(row, tx):
    for k in tx:
        row[k] = tx[k](row[k])
    return row


def _downgrade(table_obj, primary_key=None):
    bind = op.get_bind()
    key = 'id'
    if primary_key is not None:
        key = primary_key

    for row in bind.execute(table_obj.select()):
        op.execute(table_obj.delete().where(getattr(table_obj.c, key) == getattr(row, key)))
