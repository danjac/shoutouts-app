
from pyramid.authentication import (
    AuthTktAuthenticationPolicy, 
    Everyone, 
    Authenticated
)

from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import unauthenticated_userid

from .models import User
from .resources import Root


def includeme(config):

    config.set_authentication_policy(AuthenticationPolicy('seekrit'))
    config.set_authorization_policy(ACLAuthorizationPolicy())

    config.set_request_property(get_user, 'user', reify=True)
    config.set_default_permission('view')
    config.set_root_factory(Root)

 
def get_user(request):

    user_id = unauthenticated_userid(request)

    if user_id is not None:
        try:
            return User.objects.with_id(user_id)
        except ValidationError: # not a valid ObjectId
            pass




class AuthenticationPolicy(AuthTktAuthenticationPolicy):

    def effective_principals(self, request):

        principals = [Everyone]

        if request.user:
            principals.append(Authenticated)

        return principals



