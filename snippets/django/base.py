from itertools import chain

from django.db import models


class BaseModel(models.Model):

    def to_dict(self):
        opts = self._meta
        data = {}
        for field in chain(opts.concrete_fields, opts.private_fields):
            data[field.name] = field.value_from_object(self)

        for field in opts.many_to_many:
            data[field.name] = [
                inner_field.id for inner_field in field.value_from_object(self)
            ]

        return data

    class Meta:
        abstract = True
