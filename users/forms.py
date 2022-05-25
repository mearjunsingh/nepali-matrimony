from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
)

from .models import Hobby

User = get_user_model()


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    password1: forms.Field = forms.CharField(
        label="Password", widget=forms.PasswordInput()
    )
    password2: forms.Field = forms.CharField(
        label="Password Confirmation", widget=forms.PasswordInput()
    )
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = User
        fields = (
            "phone_number",
            "full_name",
            "date_of_birth",
            "profile_photo",
            "gender",
            "show",
            "password1",
            "password2",
        )


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class UserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    password = None

    profile_photo = forms.ImageField(widget=forms.FileInput(), required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={"rows": "3"}), required=False)
    hobbies = forms.ModelMultipleChoiceField(
        queryset=Hobby.objects.all(), widget=forms.SelectMultiple(), required=False
    )

    class Meta:
        model = User
        fields = ("profile_photo", "bio", "hobbies")
