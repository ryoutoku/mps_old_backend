from django.db.models import Q
from django.contrib import admin
from django.forms import ValidationError, ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import CompanyBasicInfo, CompanyStaff, Project
from authentication.models import User
from utility.admin_helper import get_model_link


class CompanyBasicInfoAdminForm(ModelForm):

    class Meta:
        model = CompanyBasicInfo
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


@admin.register(CompanyBasicInfo)
class CompanyBasicInfoAdmin(admin.ModelAdmin):
    form = CompanyBasicInfoAdminForm

    list_display = ('name', 'account_name',
                    'is_activated', 'needs_paper_invoice')
    list_filter = (NameFilter, 'is_activated', 'needs_paper_invoice',)

    def account_name(self, obj):
        account = obj.account
        return get_model_link(account, str(account))

    account_name.admin_order_field = "account"
    account_name.short_description = "登録email"


class CompanyStaffAdminForm(ModelForm):

    class Meta:
        model = CompanyStaff
        fields = "__all__"

    def clean_company(self):
        """workerが正しく設定できているかの追加確認
        """
        company = self.cleaned_data["company"]
        user = CompanyStaff.objects.filter(pk=company.id).first()

        if not user:
            raise ValidationError(_("you must set active worker"))

        return company


@admin.register(CompanyStaff)
class CompanyStaffAdmin(admin.ModelAdmin):

    list_display = ('staff_name', 'company_name',
                    'staff_department', 'staff_mail_address', )

    def staff_name(self, obj):
        return f"{obj.staff_last_name} {obj.staff_first_name}"

    def company_name(self, obj):
        company = obj.company
        return get_model_link(company, str(company))

    staff_name.admin_order_field = "staff_last_name"
    staff_name.short_description = "担当者名"

    company_name.admin_order_field = 'company'
    company_name.short_description = "企業名"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'name', 'is_open',
                    'min_fee', 'max_fee', 'start_term', 'end_term')
    list_filter = ('is_open',)

    def company_name(self, obj):
        company = obj.company
        return get_model_link(company, str(company))

    company_name.admin_order_field = 'company'
    company_name.short_description = "企業名"
