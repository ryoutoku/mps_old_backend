import secrets

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from .models import User, SignUpToken
from django import forms
from django.utils.html import format_html


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', )


class MyUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Attributes'), {'fields': ('worker', 'company',)}),
        (_('Permissions'), {'fields': (
            'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions')}),
        (_('Important dates'), {
         'fields': ('last_login', 'joined_at', 'defected_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',  "is_staff", "is_superuser"),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('email', 'worker_name',
                    'company_name', 'is_active', 'is_staff',  'defected_at')
    list_filter = ('is_staff', 'is_superuser',
                   'is_active', 'groups')
    search_fields = ('email', 'is_superuser', 'is_active')
    ordering = ('email',)

    _worker_link_format = "<a href='../../worker/worker/{}/change'>{}<\a>"
    _company_link_format = "<a href='../../company/company/{}/change'>{}<\a>"

    def worker_name(self, obj):
        if obj.worker is not None:
            return format_html(self._worker_link_format,
                               obj.worker.id, str(obj.worker))
        return None

    def company_name(self, obj):
        if obj.company is not None:
            return format_html(self._company_link_format,
                               obj.company.id, str(obj.company))
        return None


admin.site.register(User, MyUserAdmin)


@admin.register(SignUpToken)
class SignUpTokenAdmin(admin.ModelAdmin):
    """Singup用アクセストークンを管理する
    """

    list_display = ('token', 'attribute', 'expiration_date')

    fieldsets = [
        ("expiration_date", {'fields': ['attribute', 'expiration_date']}),
    ]

    def save_model(self, request, obj, form, change):

        if not obj.token:
            obj.token = secrets.token_hex(4)

        super().save_model(request, obj, form, change)
