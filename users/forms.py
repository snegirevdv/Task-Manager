from django.contrib.auth.forms import UserCreationForm
from users import models


class UserForm(UserCreationForm):
    """User creation and editing form."""

    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "username")
