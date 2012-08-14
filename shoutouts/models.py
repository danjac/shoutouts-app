import datetime
import random
import string

from pyramid.security import Allow
from pyramid.authentication import Authenticated

from cryptacular.bcrypt import BCRYPTPasswordManager

from mongoengine import (
    Document,
    EmbeddedDocument,
    StringField,
    BooleanField,
    DateTimeField,
    ReferenceField,
    ObjectIdField,
    ListField,
)

from mongoengine.queryset import QuerySet

_password_manager = BCRYPTPasswordManager()

def create_register_key(size=30):
    """
    Create a random registration key
    """
    s = string.ascii_letters + string.digits
    return "".join(random.choice(s) for i in xrange(size))

class Root(object):
    """
    Root authentication object
    """

    __acl__ = [(Allow, Authenticated, 'view')]

    def __init__(self, request):
        pass


class UserQuerySet(QuerySet):

    def authenticate(self, email, password):
        
        user = User.objects.filter(email=email, is_active=True).first()
        if user and user.check_password(password):
            return user
               

class Team(Document):
    name = StringField(unique=True, required=True)
    members = ListField(ObjectIdField)


class User(Document):

    team = ReferenceField(Team)

    email = StringField(unique=True, required=True)
    password = StringField()

    first_name = StringField(required=True)
    last_name = StringField(required=True)

    joined_on = DateTimeField(default=datetime.datetime.utcnow)

    is_active = BooleanField(default=False)
    register_key = StringField(unique=True, default=create_register_key)

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


class Shoutout(EmbeddedDocument):

    user = ReferenceField(User)
    team = ReferenceField(Team)
    reason = StringField(required=True)


class UserReport(Document):
    """
    Weekly report created by an individual user.

    This will contain the same info for everybody.
    """

    owner = ReferenceField(User)
    last_editor = ReferenceField(User)

    shoutouts = ListField(Shoutout)
    one_percents = ListField(Shoutout)

    lessons_learned = ListField(StringField())
    tasks = ListField(StringField())
    accomplishments = ListField(StringField())

    created_on = DateTimeField(default=datetime.datetime.utcnow)
    updated_on = DateTimeField(default=datetime.datetime.utcnow)

    is_complete = BooleanField(default=False)


class TeamReportField(EmbeddedDocument):
    """
    An individual field for a TeamReportForm.

    For now, we'll just use plain text fields.
    """

    name = StringField()
    title = StringField()
    required = BooleanField(default=False)


class TeamReportForm(Document):

    """
    Team reports vary per team, with different fields. This
    contains a "template" for keeping all that metadata
    together.
    """

    name = StringField(unique=True)
    title = StringField(unique=True)

    team = ReferenceField(Team, required=False)

    fields = ListField(TeamReportField)


class TeamReportItem(EmbeddedDocument):
    """
    Individual piece of data for a weekly team report.
    """

    name = StringField()
    title = StringField()
    value = StringField()

class TeamReport(Document):
    """
    Weekly team report. Contains at minimum comments, 
    but also has a set of specific fields determined 
    by its form.
    """

    last_editor = ReferenceField(User)
    form = ReferenceField(TeamReportForm)
    team = ReferenceField(Team)

    # free field
    comments = StringField()

    created_on = DateTimeField(default=datetime.datetime.utcnow)
    updated_on = DateTimeField(default=datetime.datetime.utcnow)

    is_complete = BooleanField(default=False)

    items = ListField(TeamReportItem) 

