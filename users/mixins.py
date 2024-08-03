from django.contrib import messages
from django.shortcuts import redirect
from django.views import generic

from core import consts


class OnlySelfUserCanEdit(
    generic.detail.SingleObjectMixin,
    generic.View,
):
    """Only user can edit or delete themselves."""

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user == self.get_object():
            messages.error(
                self.request,
                consts.Message.FAILURE_USER_EDIT.value,
            )
            return redirect("users:list")

        return super().dispatch(request, *args, **kwargs)
