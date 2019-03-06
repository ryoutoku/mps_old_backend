# coding: utf-8
from django.db import models
from django.utils import timezone

from worker.models import Resume
from authentication.models import User


class Question(models.Model):
    """レジュメに対する企業の質問を管理するクラス
    """
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="question",
                               verbose_name="質問したレジュメ")

    account = models.ForeignKey(User, on_delete=models.CASCADE, related_name="question",
                                verbose_name="質問した企業名")

    detail = models.TextField(verbose_name="質問内容",)

    create_at = models.DateTimeField(default=timezone.now, verbose_name="質問時間")

    def __str__(self):
        return f"{self.resume}"

    class Meta:
        ordering = ("create_at", )


class Answer(models.Model):
    """ユーザと企業とのレジュメボードでのやり取りの内容を管理するクラス
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="question",
                                 verbose_name="質問内容")

    detail = models.TextField(verbose_name="回答内容",)

    create_at = models.DateTimeField(default=timezone.now, verbose_name="回答時間")

    def __str__(self):
        return f"{self.question}"

    class Meta:
        ordering = ("create_at", )
