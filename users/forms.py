from django.contrib.auth.forms import UserCreationForm

from users import models


class UserForm(UserCreationForm):
    """User creation and editing form."""

    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "username")

    def clean_username(self):
        """When updating, the username is checked only if it was changed."""
        username = self.cleaned_data.get("username")

        if self.instance and self.instance.username == username:
            return username

        return super().clean_username()
