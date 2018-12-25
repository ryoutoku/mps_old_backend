from django.db import models

from people.models import User
from company.models import Campany

# Create your models here.


class Negotiation(models.Model):
    """ユーザと企業との交渉ボードでのやり取りの内容を管理するクラス

    """
    message = models.TextField()
    campany = models.ForeignKey("Campany", null=True, brank=True)
    user = models.ForeignKey("User", null=True, brank=True)

    created_date = models.DateTimeField(auto_now=True, auto_now_add=True)

    def __str__(self):
        return str(name)


class Resume(models.Model):
    """ユーザと企業とのレジュメボードでのやり取りの内容を管理するクラス
    """

    campany = models.ForeignKey("Campany")
    detail = models.TextField()
    is_answered = models.BooleanField(default=False)

    def __str__(self):
        return str(name)
