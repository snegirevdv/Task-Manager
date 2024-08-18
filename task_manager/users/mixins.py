import logging

from django.contrib import messages
from django.shortcuts import redirect
from django.views import generic

from task_manager.core import consts

logger = logging.getLogger(__name__)


class OnlySelfUserCanEdit(
    generic.detail.SingleObjectMixin,
    generic.View,
):
    """Only user can edit or delete themselves."""

    def dispatch(self, request, *args, **kwargs):
        current_user = self.request.user
        edited_user = self.get_object()

        if not current_user == edited_user:
            logging.warning(
                f"{current_user} is trying to change {edited_user} account.",
            )
            messages.error(
                self.request,
                consts.Message.FAILURE_USER_EDIT.value,
            )
            return redirect("users:list")

        return super().dispatch(request, *args, **kwargs)
