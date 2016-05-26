import json
from datetime import date

from liebrary.models import Author

from liebraryrest.serializers import AuthorSerializer


def test_author_json_serialization():
    auth = Author(1, 'Isaac Asimov', date(1920, 1, 2))

    expected_json = json.dumps(
        {'id': 1, 'name': "Isaac Asimov", 'birth_date': "1920-01-02"}
    )

    assert AuthorSerializer.json(auth) == expected_json


def test_author_list_json_serialization():
    authors = [Author(1, 'Isaac Asimov', date(1920, 1, 2)), Author(2, 'Mario Rossi', date(1974, 3, 5))]

    expected_json = json.dumps([
        {'id': 1, 'name': "Isaac Asimov", 'birth_date': "1920-01-02"},
        {'id': 2, 'name': "Mario Rossi", 'birth_date': "1974-03-05"}
    ])

    assert AuthorSerializer.json_list(authors) == expected_json
