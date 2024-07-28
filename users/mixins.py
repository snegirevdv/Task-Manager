from django.contrib import messages
from django.shortcuts import redirect
from django.views import generic


class OnlySelfUserCanEdit(
    generic.detail.SingleObjectMixin,
    generic.View,
):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user == self.get_object():
            messages.error(self.request, "У вас нет прав для изменения другого пользователя.")
            return redirect("users:list")

        return super().dispatch(request, *args, **kwargs)
