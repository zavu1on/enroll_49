from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponseForbidden
from django.conf import settings


class MediaAccessMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest):
        print(settings.MEDIA_URL)
        if request.path.startswith(settings.MEDIA_URL) and not request.path.startswith(settings.MEDIA_URL + 'teachers'):
            if not (request.user.is_staff and request.user.is_superuser):
                return HttpResponseForbidden(b'No Access!')

        response = self.get_response(request)

        return response
