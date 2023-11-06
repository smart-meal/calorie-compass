import mongoengine as me


class User(me.Document):
    username = me.StringField(required=True)
    password_hash = me.StringField(required=True)
