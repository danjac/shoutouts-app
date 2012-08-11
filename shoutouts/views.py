from pyramid.view import view_config
from pyramid.renderers import render

from .models import (
    Priorities,
    User
)

from .forms import (
    LoginForm,
    PrioritiesForm,
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
        print priorities.one_pc
        # priorities.save()

    else:

        print form.errors

    html = render('priorities_form.jinja2', {'form' : form}, request)

    return {'success' : is_valid, 'html' : html}
