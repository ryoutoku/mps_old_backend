from django.db import models

from people.models import User
from company.models import Company


class Negotiation(models.Model):
    """ユーザと企業との交渉ボードでのやり取りの内容を管理するクラス
    """
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at", )

    def __str__(self):
        return str(name)
