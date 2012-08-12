
from pyramid.authentication import (
    AuthTktAuthenticationPolicy, 
    Everyone, 
    Authenticated
)

from pyramid.authorization import ACLAuthorizationPolicy


class AuthenticationPolicy(AuthTktAuthenticationPolicy):

    def effective_principals(self, request):

        principals = [Everyone]

        if request.user:
            principals.append(Authenticated)

        return principals



