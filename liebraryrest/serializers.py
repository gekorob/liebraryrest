import json


class AuthorSerializer:
    @classmethod
    def _serialize(cls, author):
        d = {
            'id': author.id,
            'name': author.name,
            'birth_date': author.birth_date.isoformat()
        }
        return d

    @classmethod
    def json(cls, author):
        return json.dumps(cls._serialize(author))

    @classmethod
    def _serialize_list(cls, authors):
        return [cls._serialize(a) for a in authors]

    @classmethod
    def json_list(cls, authors):
        return json.dumps(cls._serialize_list(authors))
