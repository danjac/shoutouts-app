from pyramid.view import view_config, forbidden_view_config
from pyramid.security import NO_PERMISSION_REQUIRED, remember
from pyramid.renderers import render
from pyramid.httpexceptions import HTTPFound


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

@view_config(route_name='login',
             request_method='GET',
             permission=NO_PERMISSION_REQUIRED,
             renderer='login.jinja2')
@forbidden_view_config(renderer='login.jinja2')
def login(request):
    return {'form' : LoginForm(next=request.url)}


@view_config(route_name='login',
             request_method='POST',
             permission=NO_PERMISSION_REQUIRED,
             renderer='login.jinja2')
def do_login(request):

    form = LoginForm(request.POST)

    if form.validate():
        
        user = User.objects.authenticate(form.email.data, form.password.data)

        if user:
            headers = remember(request, str(user.id))
            return HTTPFound(form.next.data, headers=headers)

    return {'form' : form}


@view_config(route_name='submit',
             renderer='json',
             request_method='POST',
             xhr=True)
def submit(request):

    form = PrioritiesForm(request.POST)
    is_valid = form.validate()

    if is_valid:
        
        priorities = Priorities(
            owner=request.user,
            is_complete=bool(form.complete.data),
        )
        
        form.populate_obj(priorities)

        print priorities.tasks
        print priorities.one_pc
        print priorities.owner
        # priorities.save()

    else:

        print form.errors

    # re-render the form partial
    html = render('priorities_form.jinja2', {'form' : form}, request)

    return {'success' : is_valid, 'html' : html}
