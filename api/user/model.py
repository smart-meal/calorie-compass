import mongoengine as me


class User(me.Document):
    username = me.StringField(required=True)
    password_hash = me.StringField(required=True)
    salt = me.StringField(required=True)

    def to_dict(self):
        result = self.to_mongo().to_dict()
        result.pop("_id", None)
        result.pop("password_hash", None)
        result.pop("salt", None)
        result["id"] = str(self.id)  # pylint: disable=no-member
        return result
