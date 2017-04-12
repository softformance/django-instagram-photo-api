# Middleware to catch any sort of error from our views,
# and output it as either HTML or JSON appropriately

from django.http import JsonResponse
from .exceptions import JsonException


class JsonExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request, exception=None):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.


        return response

    def process_exception(self, request, exception):

        if not isinstance(exception, JsonException):
            return None

        return JsonResponse({'error': exception.message})