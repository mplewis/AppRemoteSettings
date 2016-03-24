from django.db.models import Model, TextField, IntegerField, ForeignKey


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
    name = TextField()
    desc = TextField()


class Identifier(Model):
    app = ForeignKey(App)
    desc = TextField()
    value = TextField()


class Key(Model):
    app = ForeignKey(App)
    desc = TextField()
    key = TextField()
    value = TextField()
    datatype = IntegerField(choices=DATATYPES, default=DATATYPE_BOOL)
