import mongoengine as me

class UserProfile(me.EmbeddedDocument):
    first_name = me.StringField()
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
        super().__init__(*args, **kwargs)
        if not self.user_profile:
            self.user_profile = UserProfile()

    def to_dict(self):
        result = self.to_mongo().to_dict()
        result.pop("_id", None)
        result.pop("password_hash", None)
        result.pop("salt", None)
        result["id"] = str(self.id)  # pylint: disable=no-member
        return result

class Meal(me.Document):
    title = me.StringField(required=True)
    image_url = me.StringField(required=True)
    meal_date = me.DateField(required=True)
    description = me.StringField()
    weight = me.FloatField()
    calories = me.FloatField()
    fat = me.FloatField()
    carbs = me.FloatField()
    proteins = me.FloatField()
    user = me.ReferenceField(User, reverse_delete_rule=me.CASCADE)

    def to_dict(self):
        result = self.to_mongo().to_dict()
        result.pop("_id", None)
        result["meal_date"] = result["meal_date"].strftime("%Y-%m-%d")  # Format date as string
        result["user_id"] = str(self.user.id)
        return result
