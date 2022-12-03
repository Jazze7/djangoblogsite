import json

from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from posts.models import Post


def allow_self(function):
    def wrapper(request, *args, **kwargs):
        id = kwargs["id"]
        if not Post.objects.filter(id=id, author__user=request.user).exists():
            if request.headers.get("x-request-with") == "XMLHttpRequest":
                response_data = {
                    "status": "error",
                    "title": "Unauthorized access",
                    "message": "Unauthorized access"
                }
                return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return HttpResponseRedirect(reverse("web:index"))
        return function(request, *args, **kwargs)
    return wrapper
