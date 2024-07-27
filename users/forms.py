from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class UserCreateForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        )


class UserUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "username",
        )
