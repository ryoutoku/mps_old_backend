from django.db.models import Q
from django.contrib import admin
from django.forms import ValidationError, ModelForm
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html

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


class NameFilter(admin.SimpleListFilter):
    title = _("name")
    parameter_name = 'name'

    def lookups(self, request, model_admin):
        return ((True, _("Yes")), (False, _("No")))

    def queryset(self, request, queryset):
        value = self.value()
        if value is None:
            return queryset

        if value == "True":
            return queryset.filter(~Q(name=None))

        return queryset.filter(name=None)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    form = CompanyAdminForm

    list_display = ('name', 'account_name', 'is_activate', )
    list_filter = (NameFilter, 'is_activate')

    _user_link_format = "<a href='../../certification/user/{}/change'>{}<\a>"

    def account_name(self, obj):
        return format_html(self._user_link_format, obj.account.id, str(obj.account))

    account_name.admin_order_field = "account"
    account_name.short_description = "登録email"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass
