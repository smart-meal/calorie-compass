import mongoengine as me

class UserProfile(me.EmbeddedDocument):
    first_name = me.StringField(required=True)
    last_name = me.StringField()
    age = me.IntField()
    height = me.DecimalField()
    weight = me.DecimalField()
    goal = me.StringField(choices=["Maintain weight", "Lose weight", "Gain weight"])
    lifestyle = me.StringField(choices=["Lazy", "Sedentary", "Active", "Moderate"])
    allergies = me.StringField()
    body_type = me.StringField()
    bmi = me.DecimalField()

class User(me.Document):
    username = me.StringField(required=True)
    password_hash = me.StringField(required=True)
    salt = me.StringField(required=True)
    user_profile = me.EmbeddedDocumentField(UserProfile)
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        if not self.user_profile:
            self.user_profile = UserProfile()

    def to_dict(self):
        result = self.to_mongo().to_dict()
        result.pop("_id", None)
        result.pop("password_hash", None)
        result.pop("salt", None)
        result["id"] = str(self.id)  # pylint: disable=no-member
        return result