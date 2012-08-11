from pyramid.view import view_config
from pyramid.renderers import render

from wtforms import (
    Form,
    TextField,
    PasswordField,
    SelectField,
    SubmitField,
    FieldList,
    validators,
)

from .models import (
    User,
    Priorities,
)

def get_users():
    return ((str(u.id), u.name) for u in User.objects)

class PrioritiesForm(Form):
    """
    The weekly priorities form
    """

    shoutout = SelectField(choices=get_users())

    shoutout_reason = TextField(
        validators=(
            validators.Required(),
        ),
    )

    one_pc = SelectField(choices=get_users())
    one_pc_reason = TextField()

    lessons_learned = TextField()
    tasks = FieldList(TextField(), min_entries=3)

    complete = SubmitField("I'm done")
    postpone = SubmitField("Save and finish later")


class LoginForm(Form):
    """
    Shows login
    """

    email = TextField(
        u"Email address",
        (
            validators.Required(),
            validators.Email(),
        )
    )

    password = PasswordField(
        u"Password",
        (
            validators.Required(),
        )
    )

@view_config(route_name='main', 
             renderer='index.jinja2')
def main(request):
    return {'form' : PrioritiesForm()}


@view_config(route_name='submit',
             renderer='json',
             xhr=True)
def submit(request):

    form = PrioritiesForm(request.POST)
    # normally we'd get request.user here
    user = User.objects.first()
    print "user:", user

    is_valid = form.validate()

    if is_valid:
        
        priorities = Priorities(
            owner=user,
            is_complete=bool(form.complete.data),
        )
        
        form.populate_obj(priorities)

        print priorities.tasks
        # priorities.save()

    else:

        print form.errors

    html = render('priorities_form.jinja2', {'form' : form}, request)

    return {'success' : is_valid, 'html' : html}
