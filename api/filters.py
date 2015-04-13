"""

REST API Filters
================

Borrowed from flask-peeweee with the form bits taken out.

"""

import datetime

from peewee import BigIntegerField
from peewee import BooleanField
from peewee import CharField
from peewee import DateField
from peewee import DateTimeField
from peewee import DecimalField
from peewee import DoubleField
from peewee import FloatField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import PrimaryKeyField
from peewee import TextField
from peewee import TimeField
from peewee import fn


class QueryFilter(object):
    """
    Basic class representing a named field (with or without a list of options)
    and an operation against a given value
    """

    def __init__(self, field, name, options=None):
        self.field = field
        self.name = name
        self.options = options

    def query(self, value):
        raise NotImplementedError

    def operation(self):
        raise NotImplementedError

    def get_options(self):
        return self.options


class EqualQueryFilter(QueryFilter):
    def query(self, value):
        return self.field == value

    def operation(self):
        return 'equal to'


class NotEqualQueryFilter(QueryFilter):
    def query(self, value):
        return self.field != value

    def operation(self):
        return 'not equal to'


class LessThanQueryFilter(QueryFilter):
    def query(self, value):
        return self.field < value

    def operation(self):
        return 'less than'


class LessThanEqualToQueryFilter(QueryFilter):
    def query(self, value):
        return self.field <= value

    def operation(self):
        return 'less than or equal to'


class GreaterThanQueryFilter(QueryFilter):
    def query(self, value):
        return self.field > value

    def operation(self):
        return 'greater than'


class GreaterThanEqualToQueryFilter(QueryFilter):
    def query(self, value):
        return self.field >= value

    def operation(self):
        return 'greater than or equal to'


class StartsWithQueryFilter(QueryFilter):
    def query(self, value):
        return fn.Lower(fn.Substr(self.field, 1, len(value))) == value.lower()

    def operation(self):
        return 'starts with'


class ContainsQueryFilter(QueryFilter):
    def query(self, value):
        return self.field ** ('%%%s%%' % value)

    def operation(self):
        return 'contains'


class YearFilter(QueryFilter):
    def query(self, value):
        value = int(value)
        return self.field.year == value

    def operation(self):
        return 'year equals'


class MonthFilter(QueryFilter):
    def query(self, value):
        value = int(value)
        return self.field.month == value

    def operation(self):
        return 'month equals'


class WithinDaysAgoFilter(QueryFilter):
    def query(self, value):
        value = int(value)
        return self.field >= (
            datetime.date.today() - datetime.timedelta(days=value))

    def operation(self):
        return 'within X days ago'


class OlderThanDaysAgoFilter(QueryFilter):
    def query(self, value):
        value = int(value)
        return self.field < (
            datetime.date.today() - datetime.timedelta(days=value))

    def operation(self):
        return 'older than X days ago'


class FilterMapping(object):
    """
    Map a peewee field to a list of valid query filters for that field
    """
    string = (EqualQueryFilter, NotEqualQueryFilter, StartsWithQueryFilter,
              ContainsQueryFilter)
    numeric = (EqualQueryFilter, NotEqualQueryFilter, LessThanQueryFilter,
               GreaterThanQueryFilter, LessThanEqualToQueryFilter,
               GreaterThanEqualToQueryFilter)
    datetime_date = (
        numeric +
        (WithinDaysAgoFilter, OlderThanDaysAgoFilter, YearFilter, MonthFilter))
    foreign_key = (EqualQueryFilter, NotEqualQueryFilter)
    boolean = (EqualQueryFilter, NotEqualQueryFilter)

    def get_field_types(self):
        return {
            CharField: 'string',
            TextField: 'string',
            DateTimeField: 'datetime_date',
            DateField: 'datetime_date',
            TimeField: 'numeric',
            IntegerField: 'numeric',
            BigIntegerField: 'numeric',
            FloatField: 'numeric',
            DoubleField: 'numeric',
            DecimalField: 'numeric',
            BooleanField: 'boolean',
            PrimaryKeyField: 'numeric',
            ForeignKeyField: 'foreign_key',
        }

    def convert(self, field):
        mapping = self.get_field_types()

        for klass in type(field).__mro__:
            if klass in mapping:
                mapping_fn = getattr(self, 'convert_%s' % mapping[klass])
                return mapping_fn(field)

        # fall back to numeric
        return self.convert_numeric(field)

    def convert_string(self, field):
        return [f(field, field.verbose_name, field.choices)
                for f in self.string]

    def convert_numeric(self, field):
        return [f(field, field.verbose_name, field.choices)
                for f in self.numeric]

    def convert_datetime_date(self, field):
        return [f(field, field.verbose_name, field.choices)
                for f in self.datetime_date]

    def convert_boolean(self, field):
        boolean_choices = [('True', '1', 'False', '')]
        return [f(field, field.verbose_name, boolean_choices)
                for f in self.boolean]

    def convert_foreign_key(self, field):
        return [f(field, field.verbose_name, field.choices)
                for f in self.foreign_key]


class FieldTreeNode(object):
    def __init__(self, model, fields, children=None):
        self.model = model
        self.fields = fields
        self.children = children or {}


def make_field_tree(model, fields, exclude, force_recursion=False, seen=None):
    no_explicit_fields = fields is None  # assume we want all of them
    if no_explicit_fields:
        fields = model._meta.get_field_names()
    exclude = exclude or []
    seen = seen or set()

    model_fields = []
    children = {}

    for field_obj in model._meta.get_fields():
        if field_obj.name in exclude or field_obj in seen:
            continue

        if field_obj.name in fields:
            model_fields.append(field_obj)

        if isinstance(field_obj, ForeignKeyField):
            seen.add(field_obj)
            if no_explicit_fields:
                rel_fields = None
            else:
                rel_fields = [
                    rf.replace('%s__' % field_obj.name, '')
                    for rf in fields if rf.startswith('%s__' % field_obj.name)
                ]
                if not rel_fields and force_recursion:
                    rel_fields = None

            rel_exclude = [
                rx.replace('%s__' % field_obj.name, '')
                for rx in exclude if rx.startswith('%s__' % field_obj.name)
            ]
            children[field_obj.name] = make_field_tree(field_obj.rel_model,
                                                       rel_fields, rel_exclude,
                                                       force_recursion, seen)

    return FieldTreeNode(model, model_fields, children)
