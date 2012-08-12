import datetime

from mongoengine import (
    Document,
    StringField,
    BooleanField,
    DateTimeField,
    ReferenceField,
    ListField,
)

from mongoengine.queryset import QuerySet

class UserQuerySet(QuerySet):

    def authenticate(self, email, password):
        
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            return user
               

class User(Document):

    email = StringField(unique=True, required=True)
    password = StringField()

    first_name = StringField(required=True)
    last_name = StringField(required=True)

    joined_on = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'queryset_class' : UserQuerySet}

    def __unicode__(self):
        return self.name

    @property
    def name(self):
        return " ".join((self.first_name, self.last_name))

    def check_password(self, password):
        return True


class Priorities(Document):

    owner = ReferenceField(User)

    shoutout = ReferenceField(User)
    shoutout_reason = StringField()

    one_pc = ReferenceField(User)
    one_pc_reason = StringField()

    lessons_learned = ListField(StringField())
    tasks = ListField(StringField())
    accomplishments = ListField(StringField())

    created_on = DateTimeField(default=datetime.datetime.utcnow)

    is_complete = BooleanField(default=False)

    
