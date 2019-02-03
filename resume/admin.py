from django.contrib import admin
from .models import Question, Answer

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    _link_format = "<a href='{}'>{}<\a>"

    list_display = ("id", "worker_id", "resume_id",
                    "company", "detail", "create_at")
    list_filter = ('create_at',)

    def resume_id(self, obj):
        resume = obj.resume
        url = reverse(
            f'admin:{resume._meta.app_label}_{resume._meta.model_name}_change', args=(resume.pk,)
        )

        return format_html(self._link_format, url, str(resume.id))

    def worker_id(self, obj):
        worker = obj.resume.worker
        url = reverse(
            f'admin:{worker._meta.app_label}_{worker._meta.model_name}_change', args=(worker.pk,)
        )

        return format_html(self._link_format, url, str(worker.id))


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
        company = obj.question.company
        url = reverse(
            f'admin:{company._meta.app_label}_{company._meta.model_name}_change', args=(company.pk,)
        )

        return format_html(self._link_format, url, str(company.name))

    def question(self, obj):
        question = obj.question
        url = reverse(
            f'admin:{question._meta.app_label}_{question._meta.model_name}_change', args=(question.pk,)
        )

        return format_html(self._link_format, url, str(question.detail))

    def worker_name(self, obj):
        worker = obj.question.resume.worker
        url = reverse(
            f'admin:{worker._meta.app_label}_{worker._meta.model_name}_change', args=(worker.pk,)
        )

        return format_html(self._link_format, url, str(worker))
