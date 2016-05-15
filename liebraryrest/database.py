# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related utilities."""
import json
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import relationship

from .extensions import db


# Alias common SQLAlchemy names
Column = db.Column
relationship = relationship


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True

    def serialize(self, includes=None):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    def to_json(self, includes=None):
        return json.dumps(self.serialize(includes))

    @classmethod
    def serialize_list(cls, l, includes=None):
        return [m.serialize(includes) for m in l]

    @classmethod
    def list_to_json(cls, l, includes=None):
        return json.dumps(cls.serialize_list(l, includes))
