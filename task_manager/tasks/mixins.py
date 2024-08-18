import logging

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views import generic

logger = logging.getLogger(__name__)


class OnlyAuthorCanEditMixin(
    generic.detail.SingleObjectMixin,
    generic.View,
):
    """Only task author can update or delete it."""

    author_error_message = ""
    author_error_redirect_url = ""

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user = self.request.user
        author = self.get_object().author

        if not user == author:
            logger.warning(
                f"User {user} is trying to edit a {author}'s object.",
            )
            messages.error(self.request, self.author_error_message)
            return redirect("tasks:list")

        return super().dispatch(request, *args, **kwargs)
