import datetime

from pyramid.view import view_config, forbidden_view_config
from pyramid.security import NO_PERMISSION_REQUIRED, remember, forget
from pyramid.renderers import render
from pyramid.httpexceptions import HTTPFound


from .models import (
    User,
    UserReport,
)

from .forms import (
    LoginForm,
    UserReportForm,
)

@forbidden_view_config()
def handle_forbidden(request):
    # TBD: if AJAX, just show a 403.

    request.session.flash("Sorry, you have to sign in first!")

    return HTTPFound(request.route_url('login', 
                                       _query=(('next', request.url),)))

@view_config(route_name='main', 
             renderer='index.jinja2')
def main(request):

    year, week, _ = datetime.date.today().isocalendar()

    user_report, _ = UserReport.objects.get_or_create(
        owner=request.user,
        week=week,
        year=year,
    )

    user_report_form = UserReportForm(request, obj=user_report)

    return {
            'form' : user_report_form, 
            'report' : user_report,
            }


def create_metrics_form(request, doc):
    # does the user have permission?
    # assume so for this bit

    class MetricsForm(BaseMetricsForm):
        pass

    for field in doc.template.fields:
        setattr(MetricsForm, field.name, TextField(field.title())) 

    kw = {}

    for entry in doc.entries:
        kw[entry.name] = entry.value

    return MetricsForm(request, obj=doc, **kw)


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

    if form.validate():
        
        user = User.objects.authenticate(form.email.data, form.password.data)

        if user:
            headers = remember(request, str(user.id))
            return HTTPFound(form.next.data, headers=headers)
        else:
            request.session.flash("Incorrect email or password")

    else:
        print form.errors

    return {'form' : form}


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
    user.register_key = None # forces reset
    user.save()

    request.session.flash("Thanks for signing up, %s! Now you can get "
                          "started." % user.first_name)

    headers = remember(request, str(user.id))
    return HTTPFound(request.route_url('main'), headers=headers)


@view_config(route_name="recover_pass",
             permission=NO_PERMISSION_REQUIRED,
             renderer="recover_pass.jinja2")
def recover_password(request):

    form = RecoverPasswordForm(request)
    if form.validate():

        user = User.objects.filter(email=form.email.data).first()
        if user:
            emails.send_recover_password(request, user)
            return HTTPFound(request.route_url("recover_pass_done"))
    return {'form' : form}


@view_config(route_name="change_pass",
             permission=NO_PERMISSION_REQUIRED,
             renderer="change_pass.jinja2")
def change_password(request):

    if request.user:
        user = request.user
    else:
        key = request.params.get('rkey', None)
        user = User.objects.filter(register_key=key).first()
    
    if user is None:
        raise HTTPNotFound()

    form = ChangePasswordForm(request)

    if form.validate():

        user.set_password(form.password.data)
        user.register_key = None
        user.save()

        request.session.flash("Your password has been changed, please "
                              "sign in again")

        headers = forget(request)
        return HTTPFound(request.route_url("login"), headers=headers)

    return {'form' : form}




@view_config(route_name='edit',
             renderer='json',
             request_method='POST',
             xhr=True)
def edit(report, request):

    # check if locked
    form = UserReportForm(request, obj=report)
    is_valid = form.validate()

    if not is_valid:
        print form.errors

    # re-render the form partial

    html = render('user_report_form.jinja2', {
                  'form' : form, 
                  'report' : report}, request)

    
    return {'success' : is_valid, 'html' : html}


