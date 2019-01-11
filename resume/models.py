from django.db import models

from worker.models import Worker
from company.models import Company


class Resume(models.Model):
    """ユーザと企業とのレジュメボードでのやり取りの内容を管理するクラス
    """

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="question",
                                verbose_name="質問した企業名")
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name="question",
                               verbose_name="質問されたユーザ")
    detail = models.TextField(
        verbose_name="質問内容",)
    is_answered = models.BooleanField(default=False,
                                      verbose_name="回答したか否か")

    def __str__(self):
        return f"{self.worker},{self.company}"
