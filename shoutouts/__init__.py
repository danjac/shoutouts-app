from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import unauthenticated_userid


from mongoengine import connect, ValidationError

from .models import User, Root
from .auth import AuthenticationPolicy

def get_user(request):

    user_id = unauthenticated_userid(request)

    if user_id is not None:
        try:
            return User.objects.with_id(user_id)
        except ValidationError: # not a valid ObjectId
            pass


    
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # mongoengine
    connect(settings['db_name'])

    config = Configurator(
        settings=settings,
        authentication_policy=AuthenticationPolicy('seekrit'),
        authorization_policy=ACLAuthorizationPolicy(),
    )

    # auth/auth
    config.set_request_property(get_user, 'user', reify=True)
    config.set_default_permission('view')
    config.set_root_factory(Root)

    # webassets
    config.include('shoutouts.assets')

    # routes
    config.include('shoutouts.routes')
    
    config.scan()
    return config.make_wsgi_app()
