from django.contrib import admin
from .models import Worker, WorkerBank, Resume


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkerBank)
class WorkerBankAdmin(admin.ModelAdmin):
    pass


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    pass
