from django.db import models

from people.models import User
from company.models import Company


class Negotiation(models.Model):
    """ユーザと企業との交渉ボードでのやり取りの内容を管理するクラス
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True,
        verbose_name="交渉企業", related_name="negotiation")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
        verbose_name="交渉ユーザ", related_name="negotiation")
    message = models.TextField(
        verbose_name="メッセージ内容")
    created_at = models.DateTimeField(auto_now_add=True,
        verbose_name="メッセージ作成時間")

    class Meta:
        ordering = ("created_at", )

    def __str__(self):
        return f"{self.user}, {self.company}"
