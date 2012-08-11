import datetime

from mongoengine import (
    Document,
    StringField,
    BooleanField,
    DateTimeField,
    ReferenceField,
    ListField,
)

class User(Document):

    email = StringField(unique=True, required=True)
    password = StringField()

    first_name = StringField(required=True)
    last_name = StringField(required=True)

    joined_on = DateTimeField(default=datetime.datetime.utcnow)

    def __unicode__(self):
        return self.name

    @property
    def name(self):
        return " ".join((self.first_name, self.last_name))


class Priorities(Document):

    owner = ReferenceField(User)

    shoutout = ReferenceField(User)
    shoutout_reason = StringField()

    one_pc = ReferenceField(User)
    one_pc_reason = StringField()

    lessons_learned = StringField()

    tasks = ListField(StringField())

    created_on = DateTimeField(default=datetime.datetime.utcnow)

    is_complete = BooleanField(default=False)

    
