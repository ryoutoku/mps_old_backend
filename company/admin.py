from django.contrib import admin
from .models import Company, Project


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass
