from django.contrib import messages
from django.shortcuts import redirect
from django.views import generic
from django.utils.translation import gettext_lazy as _


class OnlySelfUserCanEdit(
    generic.detail.SingleObjectMixin,
    generic.View,
):
    """Only user can edit or delete themselves."""

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user == self.get_object():
            messages.error(
                self.request,
                _("You do not have permission to edit another user."),
            )
            return redirect("users:list")

        return super().dispatch(request, *args, **kwargs)
