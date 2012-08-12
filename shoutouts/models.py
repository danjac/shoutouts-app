import datetime

from pyramid.security import Allow
from pyramid.authentication import Authenticated

from cryptacular.bcrypt import BCRYPTPasswordManager

from mongoengine import (
    Document,
    StringField,
    BooleanField,
    DateTimeField,
    ReferenceField,
    ListField,
)

from mongoengine.queryset import QuerySet

_password_manager = BCRYPTPasswordManager()

class Root(object):
    """
    Root authentication object
    """

    __acl__ = [(Allow, Authenticated, 'view')]

    def __init__(self, request):
        pass


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

    def set_password(self, password):
        self.password = _password_manager.encode(password)

    def check_password(self, password):
        return _password_manager.check(self.password, password)


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

    
