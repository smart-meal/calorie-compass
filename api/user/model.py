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
    """
    Represents a user document in MongoDB using MongoEngine.

    """
    username = me.StringField(required=True)
    """The username of the user. """
    password_hash = me.StringField(required=True) 
    """The hashed password of the user. """
    salt = me.StringField(required=True)
    """The random salt generated when register in password hashing. """
    user_profile = me.EmbeddedDocumentField(UserProfile)
    """User Profile """

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        if not self.user_profile:
            self.user_profile = UserProfile()

    def to_dict(self):
        """
        Converts the User document to a dictionary.

        This method is used to serialize the User object to a dictionary format,
        password hash and salt are not included.

        Returns:
            dict: A dictionary representation of the User object without sensitive data.
        """
        result = self.to_mongo().to_dict()
        result.pop("_id", None)
        result.pop("password_hash", None)
        result.pop("salt", None)
        result["id"] = str(self.id)  # pylint: disable=no-member
        return result