from django.contrib import admin
from .models import User, Career


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    pass
