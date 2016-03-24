from django.db.models import Model, CharField, IntegerField, ForeignKey


DATATYPE_BOOL = 1
DATATYPE_INT = 2
DATATYPE_FLOAT = 3
DATATYPE_STRING = 4
DATATYPES = (
    (DATATYPE_BOOL, "Boolean"),
    (DATATYPE_INT, "Integer"),
    (DATATYPE_FLOAT, "Float"),
    (DATATYPE_STRING, "String"),
)


class App(Model):
    name = CharField(max_length=255)
    desc = CharField(max_length=255, verbose_name='description')

    def __str__(self):
        return '{} - {}'.format(self.name, self.desc)


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
