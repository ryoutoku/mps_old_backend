from django.db import models
from django.utils import timezone

from certification.models import User


class Company(models.Model):
    """企業の情報を管理するクラス
    """

    account = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company',
                                   verbose_name="アカウント情報", null=True, blank=True, unique=True)

    is_activate = models.BooleanField(default=False,
                                      verbose_name="入力が完了したか否か")

    name = models.CharField(max_length=50, null=True, blank=True,
                            verbose_name="企業名")

    staff_name = models.CharField(max_length=50, null=True, blank=True,
                                  verbose_name="担当者名")

    phone_number = models.CharField(max_length=50, null=True, blank=True,
                                    verbose_name="電話番号")

    address = models.CharField(max_length=50, null=True, blank=True,
                               verbose_name="企業住所")

    closest_station_1 = models.CharField(max_length=50, null=True, blank=True,
                                         verbose_name="最寄り駅1")

    closest_station_2 = models.CharField(max_length=50, null=True, blank=True,
                                         verbose_name="最寄り駅2")

    needs_paper_invoice = models.BooleanField(default=False, null=True, blank=True,
                                              verbose_name="紙ベース請求書要否")

    corporate_url = models.URLField(null=True, blank=True,
                                    verbose_name="企業のコーポレートURL")

    start_office_hours = models.TimeField(null=True, blank=True,
                                          verbose_name="就業の開始時間")

    end_office_hours = models.TimeField(null=True, blank=True,
                                        verbose_name="就業の終了時間")

    contact_staff = models.CharField(max_length=50, null=True, blank=True,
                                     verbose_name="請求書宛先担当者")

    contact_staff_mail_address = models.CharField(max_length=50, null=True, blank=True,
                                                  verbose_name="請求書宛先メールアドレス")

    pr_comment = models.TextField(null=True, blank=True,
                                  verbose_name="企業のPRコメント")

    pr_photo_1 = models.ImageField(upload_to='uploads/company/image', null=True, blank=True,
                                   verbose_name="企業のPR写真1")

    pr_photo_2 = models.ImageField(upload_to='uploads/company/image', null=True, blank=True,
                                   verbose_name="企業のPR写真2")

    joined_date = models.DateTimeField(default=timezone.now,
                                       verbose_name="入会年月日")

    defected_date = models.DateField(null=True, blank=True,
                                     verbose_name="退会年月日")

    def __str__(self):
        return f"{self.name}"


class Project(models.Model):
    """案件を表すクラス
    """

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='project',
        verbose_name="企業")

    name = models.CharField(max_length=16,
                            verbose_name="案件名")

    min_fee = models.IntegerField(null=True, blank=True,
                                  verbose_name="最小単金")

    max_fee = models.IntegerField(null=True, blank=True,
                                  verbose_name="最大単金")

    workplace = models.CharField(max_length=16, null=True, blank=True,
                                 verbose_name="作業場所(住所/ビル名など)")

    closest_station = models.CharField(max_length=50, null=True, blank=True,
                                       verbose_name="最寄り駅")

    start_term = models.DateField(null=True, blank=True,
                                  verbose_name="開始時期(xxxx年mm月)")

    end_term = models.DateField(null=True, blank=True,
                                verbose_name="終了時間(xxxx年mm月)")

    start_time = models.TimeField(null=True, blank=True,
                                  verbose_name="就業開始時間")

    end_time = models.TimeField(null=True, blank=True,
                                verbose_name="就業終了時間")

    rest_time = models.TimeField(null=True, blank=True,
                                 verbose_name="就業中の休憩時間")

    garments = models.CharField(max_length=16, null=True, blank=True,
                                verbose_name="服装")

    restroom = models.CharField(max_length=16, null=True, blank=True,
                                verbose_name="トイレ")

    conditions = models.CharField(max_length=16, null=True, blank=True,
                                  verbose_name="条件備考")

    content = models.TextField(null=True, blank=True,
                               verbose_name="作業内容")

    appeal = models.TextField(null=True, blank=True,
                              verbose_name="作業のアピール点")

    required_skills = models.TextField(null=True, blank=True,
                                       verbose_name="必須スキル")

    preferred_skills = models.TextField(null=True, blank=True,
                                        verbose_name="尚可スキル")

    def __str__(self):
        return f"{self.name}"
