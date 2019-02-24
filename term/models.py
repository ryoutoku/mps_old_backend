from django.db import models
from django.utils import timezone


TYPE_CHOICES = {
    ('企業', '企業用'),
    ('メンバー', 'メンバー用'),
}


class ServiceOfTerm(models.Model):

    target_type = models.CharField(choices=TYPE_CHOICES, default="企業", max_length=10,
                                   verbose_name="利用規約の提示先")

    context = models.TextField(verbose_name="利用規約")

    create_at = models.DateTimeField(default=timezone.now, verbose_name="公開時間")

    def __str__(self):
        return f"{self.context}"


class PrivacyPolicy(models.Model):

    target_type = models.CharField(choices=TYPE_CHOICES, default="企業", max_length=10,
                                   verbose_name="利用規約の提示先")

    context = models.TextField(verbose_name="プライバシーポリシー")

    create_at = models.DateTimeField(default=timezone.now, verbose_name="公開時間")

    def __str__(self):
        return f"{self.context}"
