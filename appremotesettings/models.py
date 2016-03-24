from django.db.models import Model, TextField, IntegerField, ForeignKey


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
    datatype = IntegerField()
