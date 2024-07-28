from django.contrib import messages
from django.contrib.auth import mixins
from django.shortcuts import redirect
from django.views import generic


class OnlyAuthorCanEditMixin(
    mixins.UserPassesTestMixin,
    generic.detail.SingleObjectMixin,
    generic.View,
):
    author_error_message = ""
    author_error_redirect_url = ""

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user == self.get_object().author:
            messages.error(self.request, self.author_error_message)
            return redirect(self.author_error_redirect_url)

        return super().dispatch(request, *args, **kwargs)
