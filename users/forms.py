from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth import get_user_model


User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Phone Number', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id' : 'id_phone_number',
            'placeholder': '98*********',
            'autofocus' : 'true'
            }
        ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '********'
            }
        ))


class UserChangeForm(UserChangeForm):
    password = None
    
    class Meta:
        model = User
        fields = ['profile_photo', 'bio', 'hobbies']
        widgets = {
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 80px;'}),
            'hobbies': forms.CheckboxSelectMultiple(),
        }