from django.db.models import Model, CharField, IntegerField, ForeignKey
from django.core.exceptions import ValidationError

import dateutil.parser
from django.template.defaultfilters import pluralize

DATATYPE_BOOL = 1
DATATYPE_INT = 2
DATATYPE_FLOAT = 3
DATATYPE_STRING = 4
DATATYPE_DATE = 5
DATATYPES = (
    (DATATYPE_BOOL, "Boolean"),
    (DATATYPE_INT, "Integer"),
    (DATATYPE_FLOAT, "Float"),
    (DATATYPE_STRING, "String"),
    (DATATYPE_DATE, "Date"),
)
DATATYPE_SLUGS = {
    DATATYPE_BOOL: "bool",
    DATATYPE_INT: "int",
    DATATYPE_FLOAT: "float",
    DATATYPE_STRING: "string",
    DATATYPE_DATE: "date"
}


def cast(raw, to):
    if to == DATATYPE_BOOL:
        raw = raw.lower().strip()
        if raw == 'true':
            return True
        elif raw == 'false':
            return False
        else:
            raise ValueError('{} must be "true" or "false"'.format(raw))
    elif to == DATATYPE_INT:
        return int(raw)
    elif to == DATATYPE_FLOAT:
        return float(raw)
    elif to == DATATYPE_STRING:
        return str(raw)
    elif to == DATATYPE_DATE:
        return dateutil.parser.parse(raw)


class App(Model):
    name = CharField(max_length=255)
    desc = CharField(max_length=255, verbose_name='description', blank=True)

    def __str__(self):
        kc = self.key_set.count()
        if not self.desc:
            return '{} ({} key{})'.format(self.name, kc, pluralize(kc))
        return '{} ({} key{}) - {}'.format(self.name, kc, pluralize(kc), self.desc)

    def typed_keys(self):
        return {key.key: key.typed_value() for key in self.key_set.all()}


class Identifier(Model):
    app = ForeignKey(App)
    desc = CharField(max_length=255, verbose_name='description', blank=True)
    value = CharField(max_length=255, unique=True)

    def __str__(self):
        if not self.desc:
            return self.value
        return '{} ({})'.format(self.desc, self.value)


class Key(Model):
    app = ForeignKey(App)
    desc = CharField(max_length=255, verbose_name='description', blank=True)
    key = CharField(max_length=255)
    value = CharField(max_length=255)
    datatype = IntegerField(choices=DATATYPES, default=DATATYPE_BOOL, verbose_name='data type')

    def __str__(self):
        if not self.desc:
            return '{}: {}'.format(self.key, self.value)
        return '{} ({}: {})'.format(self.desc, self.key, self.value)

    def clean(self):
        try:
            self.value = self.typed_value()
        except ValueError as e:
            raise ValidationError(str(e))
        # Ensure dates get serialized as ISO 8601
        if self.datatype == DATATYPE_DATE:
            self.value = self.value.isoformat()

    def typed_value(self):
        return cast(self.value, self.datatype)
