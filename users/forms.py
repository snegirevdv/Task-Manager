from django.contrib.auth.forms import UserCreationForm
from users import models


class UserForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = (
            "first_name",
            "last_name",
            "username",
        )
