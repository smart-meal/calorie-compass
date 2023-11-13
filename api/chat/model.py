import datetime
from enum import Enum

import mongoengine as me


class MessageType(Enum):
    USER = 'user'
    ASSISTANT = 'assistant'
    SYSTEM = 'system'

    @classmethod
    def get_all_types(cls):
        return [e.value for e in cls]


class Message(me.Document):
    text = me.StringField(required=True)
    type = me.EnumField(required=True, enum=MessageType)
    date = me.DateTimeField(required=True, default=datetime.datetime.utcnow)
    user_id = me.ReferenceField(required=True, document_type="User", dbref=False)

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        self.date = datetime.datetime.now(datetime.timezone.utc)

    def to_dict(self):
        result = self.to_mongo().to_dict()
        result.pop("_id", None)
        result["id"] = str(self.id)  # pylint: disable=no-member
        return result
