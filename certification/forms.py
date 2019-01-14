from django import forms
from .models import User


class UserModelForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("email", "password")

    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'email-address'})
        )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'password'}),
        min_length=6
        )