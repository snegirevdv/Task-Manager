from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views import generic


class OnlyAuthorCanEditMixin(
    generic.detail.SingleObjectMixin,
    generic.View,
):
    """Only task author can update or delete it."""

    author_error_message = ""
    author_error_redirect_url = ""

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not self.request.user == self.get_object().author:
            messages.error(self.request, self.author_error_message)
            return redirect(self.author_error_redirect_url)

        return super().dispatch(request, *args, **kwargs)
