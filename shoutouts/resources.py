from pyramid.security import Allow
from pyramid.authentication import Authenticated

from .models import UserReport

class Root(object):
    """
    Root authentication object
    """

    __acl__ = [(Allow, Authenticated, 'view')]

    def __init__(self, request):
        pass



class DocumentFactory(object):

    model = None

    def __init__(self, request):
        self.request = request

    def __getitem__(self, key):
        return self.get_doc(key)

    def get_doc(self, key):
        return self.model.objects.with_id(key)


class UserReportFactory(DocumentFactory):

    model = UserReport



