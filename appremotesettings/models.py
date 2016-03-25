from django.db.models import Model, CharField, IntegerField, ForeignKey

import dateutil.parser


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


class App(Model):
    name = CharField(max_length=255)
    desc = CharField(max_length=255, verbose_name='description')

    def __str__(self):
        return '{} - {}'.format(self.name, self.desc)

    def typed_keys(self):
        return {key.key: key.typed_value() for key in self.key_set.all()}


class Identifier(Model):
    app = ForeignKey(App)
    desc = CharField(max_length=255, verbose_name='description')
    value = CharField(max_length=255)

    def __str__(self):
        return '{} - {} ({})'.format(self.app.name, self.desc, self.value)


class Key(Model):
    app = ForeignKey(App)
    desc = CharField(max_length=255, verbose_name='description')
    key = CharField(max_length=255)
    value = CharField(max_length=255)
    datatype = IntegerField(choices=DATATYPES, default=DATATYPE_BOOL, verbose_name='data type')

    def __str__(self):
        return '{} - {} ({}: {})'.format(self.app.name, self.desc, self.key, self.value)

    def typed_value(self):
        if self.datatype == DATATYPE_BOOL:
            if 'true' in self.value.lower().strip():
                return True
            else:
                return False
        elif self.datatype == DATATYPE_INT:
            return int(self.value)
        elif self.datatype == DATATYPE_FLOAT:
            return float(self.value)
        elif self.datatype == DATATYPE_STRING:
            return self.value
        elif self.datatype == DATATYPE_DATE:
            return dateutil.parser.parse(self.value)
