import mongoengine as me


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
