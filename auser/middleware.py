import datetime

from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.core.cache import cache
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

from django.contrib.auth import get_user_model

User = get_user_model()


def get_user_jwt(request):
    user = None
    try:
        user_jwt = JWTAuthentication().authenticate(Request(request))
        # print(user_jwt)
        if user_jwt is not None:
            # store the first part from the tuple (user, obj)
            user = user_jwt[0]
    except:
        pass

    return user or AnonymousUser()


class ActiveUserMiddleware(MiddlewareMixin):
    """ Middleware for authenticating JSON Web Tokens in Authorize Header """

    def process_request(self, request):
        if not request.user.is_authenticated:
            request.user = SimpleLazyObject(lambda: get_user_jwt(request))
            current_user = request.user
            if request.user.is_authenticated:
                now = datetime.datetime.now()
                cache.set('seen_%s' % current_user.email, now, settings.USER_LASTSEEN_TIMEOUT)

# This middleware for session auth
# class ActiveUserMiddleware(MiddlewareMixin):
#
#     def process_request(self, request):
#         current_user = request.user
#         print(request.user)
#         if request.user.is_authenticated:
#             now = datetime.datetime.now()
#             cache.set('seen_%s' % current_user.email, now, settings.USER_LASTSEEN_TIMEOUT)
#             print(cache.get('seen_%s' % current_user), current_user)
