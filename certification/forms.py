from django import forms
from django.forms import inlineformset_factory
from .models import User

from worker.models import Worker
from company.models import Company


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


class WorkerModelForm(UserModelForm):
    def save(self, commit=True):
        user = super().save(commit=True)
        worker = Worker.objects.create(account=user)
        worker.save()
        return user


class CompanyModelForm(UserModelForm):
    def save(self, commit=True):
        user = super().save(commit=True)
        company = Company.objects.create(account=user)
        company.save()
        return user
