from pyramid.view import view_config, forbidden_view_config
from pyramid.security import NO_PERMISSION_REQUIRED, remember, forget
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

@forbidden_view_config()
def handle_forbidden(request):

    request.session.flash("Sorry, you have to sign in first!")

    return HTTPFound(request.route_url('login', 
                                       _query=(('next', request.url),)))

@view_config(route_name='main', 
             renderer='index.jinja2')
def main(request):
    return {'form' : PrioritiesForm(request)}

@view_config(route_name='logout')
def logout(request):

    headers = forget(request)
    return HTTPFound(request.route_url('main'), headers=headers)


@view_config(route_name='login',
             permission=NO_PERMISSION_REQUIRED,
             renderer='login.jinja2')
def login(request):

    next_url = request.params.get('next', request.route_url('main'))
    form = LoginForm(request, next=next_url)
    login_failed = False

    if form.validate():
        
        user = User.objects.authenticate(form.email.data, form.password.data)

        if user:
            headers = remember(request, str(user.id))
            return HTTPFound(form.next.data, headers=headers)
        else:
            login_failed = True

    return {'form' : form, 'login_failed' : login_failed}


@view_config(route_name="signup",
             permission=NO_PERMISSION_REQUIRED,
             renderer='signup.jinja2')
def signup(request):
    form = SignupForm(request)

    if form.validate():

        user = User(email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data)

        user.set_password(form.password.data)
        user.save()

        # emails.send_signup_confirmation(request, user)

        return HTTPFound(request.route_url('signup_done'))

    return {'form' : form}



@view_config(route_name="signup_done",
             permission=NO_PERMISSION_REQUIRED,
             renderer="signup_done.jinja2")
def signup_done(request):
    return {}


@view_config(route_name="confirm_signup",
             permission=NO_PERMISSION_REQUIRED)
def confirm_signup(request):

    key = request.params.get('rkey', None)
    if key is None:
        raise HTTPNotFound()

    try:
        user = User.objects.get(is_active=False, register_key=key)
    except DoesNotExist:
        raise HTTPNotFound()
                
    user.is_active = True
    user.register_key = None
    user.save()

    request.session.flash("Thanks! You have successfully registered. "
                          "Please sign in to Shoutouts")

    return HTTPFound(request.route_url('login'))


@view_config(route_name='submit',
             renderer='json',
             request_method='POST',
             xhr=True)
def submit(request):

    # check if locked
    form = PrioritiesForm(request)
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

    # re-render the form partial
    html = render('submit_form.jinja2', {'form' : form}, request)

    return {'success' : is_valid, 'html' : html}
