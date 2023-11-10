import mongoengine as me


class User(me.Document):
    username = me.StringField(required=True)
    password_hash = me.StringField(required=True)

    def to_dict(self):
        result = self.to_mongo().to_dict()
        result.pop("_id", None)
        result["id"] = str(self.id)
        return result
