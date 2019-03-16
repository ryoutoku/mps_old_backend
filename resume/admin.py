from django.contrib import admin
from .models import Question, Answer

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from utility.admin_helper import get_model_link


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    list_display = ("id", "worker_id", "resume_id",
                    "account", "detail", "create_at")
    list_filter = ('create_at',)

    def resume_id(self, obj):
        resume = obj.resume
        return get_model_link(resume, str(resume))

    def worker_id(self, obj):
        account = obj.resume.account
        return get_model_link(account, str(account))


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):

    list_display = ("id", "worker_name", "company_name", "question",
                    "detail", "create_at")
    list_filter = ('create_at',)

    def question_id(self, obj):
        question = obj.question
        return get_model_link(question, str(question.id))

    def company_name(self, obj):
        account = obj.question.account
        return get_model_link(account, str(account.name))

    def question(self, obj):
        question = obj.question
        return get_model_link(question, str(question.detail))

    def worker_name(self, obj):
        account = obj.question.resume.account
        return get_model_link(account, str(account))
