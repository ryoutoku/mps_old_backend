from django import forms
from django.forms import inlineformset_factory
from .models import User

from worker.models import Worker
from company.models import Company


class ModelFormWithFormSetMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formset = self.formset_class(
            instance=self.instance,
            data=self.data if self.is_bound else None,
        )

    def is_valid(self):
        return super().is_valid() and self.formset.is_valid()


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


WorkerFormSet = inlineformset_factory(
    parent_model=Worker,
    model=User,
    form=UserModelForm,
    extra=1,
    can_delete=False
)


class WorkerModelForm(ModelFormWithFormSetMixin, forms.ModelForm):
    formset_class = WorkerFormSet

    class Meta:
        model = Worker
        fields = ()

    def save(self, commit=True):
        saved_instance = super().save(commit=True)
        instance = self.formset.save()
        instance[0].worker = saved_instance
        instance[0].save()

        return saved_instance


CompanyFormSet = inlineformset_factory(
    parent_model=Company,
    model=User,
    form=UserModelForm,
    extra=3


)


class CompanyModelForm(ModelFormWithFormSetMixin, forms.ModelForm):
    formset_class = CompanyFormSet

    class Meta:
        model = User
        fields = ()

    def save(self, commit=True):
        saved_instance = super().save(commit)
        instance = self.formset.save(commit)
        instance[0].company = saved_instance
        instance[0].save()
        return saved_instance
