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

class Meal(me.Document):
    title = me.StringField(required=True)
    meal_date = me.DateField(required=True)
    description = me.StringField()
    weight = me.FloatField()
    calories = me.FloatField()
    fat = me.FloatField()
    carbs = me.FloatField()
    proteins = me.FloatField()
    picture_url = me.StringField()
    user = me.ReferenceField(User, reverse_delete_rule=me.CASCADE)

    def to_dict(self):
        result = self.to_mongo().to_dict()
        result.pop("_id", None)
        result["meal_date"] = result["meal_date"].strftime("%Y-%m-%d")  # Format date as string
        result["user_id"] = str(self.user.id)
        return result
