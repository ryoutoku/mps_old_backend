from django.contrib import admin
from .models import Question, Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    _user_link_format = "<a href='../../certification/user/{}/change'>{}<\a>"

    list_display = ("resume", "company", "detail", "create_at")
    list_filter = ('create_at',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass
