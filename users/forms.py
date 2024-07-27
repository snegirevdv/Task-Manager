from django.contrib.auth import forms, get_user_model


class UserForm(forms.UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        )
