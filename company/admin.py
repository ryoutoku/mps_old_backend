from django.contrib import admin
from django.forms import ValidationError, ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import Company, Project
from certification.models import User


class CompanyAdminForm(ModelForm):

    class Meta:
        model = Company
        fields = "__all__"

    def clean_account(self):
        """accountが正しく設定できているかの追加確認
        """

        account = self.cleaned_data["account"]
        user = User.objects.filter(email=account).first()

        if not user:
            raise ValidationError(_("you must set active account"))

        if not user.is_active:
            raise ValidationError(_("you must set active account"))

        if user.is_staff or user.is_superuser:
            raise ValidationError(_("you must set general account"))

        if hasattr(user, 'worker'):
            raise ValidationError(_("you must set worker account"))

        return account


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass
