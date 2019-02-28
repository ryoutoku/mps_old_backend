from django.contrib import admin
from .models import Question, Answer

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    _link_format = "<a href='{}'>{}<\a>"

    list_display = ("id", "worker_id", "resume_id",
                    "account", "detail", "create_at")
    list_filter = ('create_at',)

    def resume_id(self, obj):
        resume = obj.resume
        url = reverse(
            f'admin:{resume._meta.app_label}_{resume._meta.model_name}_change', args=(resume.pk,)
        )

        return format_html(self._link_format, url, str(resume.id))

    def worker_id(self, obj):
        account = obj.resume.account
        url = reverse(
            f'admin:{account._meta.app_label}_{account._meta.model_name}_change', args=(account.pk,)
        )

        return format_html(self._link_format, url, str(account.id))


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):

    _link_format = "<a href='{}'>{}<\a>"

    list_display = ("id", "worker_name", "company_name", "question",
                    "detail", "create_at")
    list_filter = ('create_at',)

    def question_id(self, obj):
        question = obj.question
        url = reverse(
            f'admin:{question._meta.app_label}_{question._meta.model_name}_change', args=(question.pk,)
        )

        return format_html(self._link_format, url, str(question.id))

    def company_name(self, obj):
        account = obj.question.account
        url = reverse(
            f'admin:{account._meta.app_label}_{account._meta.model_name}_change', args=(account.pk,)
        )

        return format_html(self._link_format, url, str(account.name))

    def question(self, obj):
        question = obj.question
        url = reverse(
            f'admin:{question._meta.app_label}_{question._meta.model_name}_change', args=(question.pk,)
        )

        return format_html(self._link_format, url, str(question.detail))

    def worker_name(self, obj):
        account = obj.question.resume.account
        url = reverse(
            f'admin:{account._meta.app_label}_{account._meta.model_name}_change', args=(account.pk,)
        )

        return format_html(self._link_format, url, str(account))
