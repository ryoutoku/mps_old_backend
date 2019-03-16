from django.db import models
from django.utils import timezone

from authentication.models import User

GARMENTS_CHOICES = (
    (0, '---未登録---'),
    (1, '規定あり'),
    (2, '私服OK'),
    (3, '要相談'),
)

RESTROOM_CHOICES = (
    (0, '---未登録---'),
    (1, '男女別'),
    (2, '男女共用'),
)

USE_CHOICES = (
    (0, '---未登録---'),
    (1, '利用可'),
    (2, '利用不可'),
)


class CompanyBasicInfo(models.Model):
    """企業の基本情報を管理するクラス
    """

    account = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company',
                                   verbose_name="Companyのアカウント", null=True, blank=True, unique=True)

    is_activated = models.BooleanField(default=False,
                                       verbose_name="入力が完了したか否か")

    name = models.CharField(max_length=50, null=True, blank=True,
                            verbose_name="企業名")

    representative_name = models.CharField(max_length=10, null=True, blank=True,
                                           verbose_name="代表者氏名")

    establishment_date = models.DateField(null=True, blank=True,
                                          verbose_name="設立日")

    capital = models.IntegerField(null=True, blank=True,
                                  verbose_name="資本金")

    sales = models.IntegerField(null=True, blank=True,
                                verbose_name="売上高")

    employee_number = models.IntegerField(null=True, blank=True,
                                          verbose_name="従業員数")

    average_age = models.IntegerField(null=True, blank=True,
                                      verbose_name="平均年齢")

    phone_number = models.CharField(max_length=20, null=True, blank=True,
                                    verbose_name="電話番号")

    address = models.CharField(max_length=50, null=True, blank=True,
                               verbose_name="企業住所")

    closest_station_1 = models.CharField(max_length=20, null=True, blank=True,
                                         verbose_name="最寄り駅1")

    closest_station_2 = models.CharField(max_length=20, null=True, blank=True,
                                         verbose_name="最寄り駅2")

    corporate_url = models.URLField(null=True, blank=True,
                                    verbose_name="企業のコーポレートURL")

    pr_comment = models.TextField(null=True, blank=True,
                                  verbose_name="企業のPRコメント")

    pr_photo_1 = models.ImageField(upload_to='uploads/company/image', null=True, blank=True,
                                   verbose_name="企業のPR写真1")

    pr_photo_2 = models.ImageField(upload_to='uploads/company/image', null=True, blank=True,
                                   verbose_name="企業のPR写真2")

    def __str__(self):
        return f"{self.name}"


class CompanyStaff(models.Model):
    """企業の担当者など、Workerから検索されない情報を保存
    """
    company = models.ForeignKey(CompanyBasicInfo, on_delete=models.CASCADE, related_name='staff',
                                verbose_name="担当者情報")

    staff_last_name = models.CharField(max_length=10, null=True, blank=True,
                                       verbose_name="担当者:姓")

    staff_first_name = models.CharField(max_length=10, null=True, blank=True,
                                        verbose_name="担当者:名")

    staff_department = models.CharField(max_length=20, null=True, blank=True,
                                        verbose_name="担当者所属部署")

    staff_mail_address = models.EmailField(null=True, blank=True,
                                           verbose_name="請求書宛先メールアドレス")

    needs_paper_invoice = models.BooleanField(default=False, null=True, blank=True,
                                              verbose_name="紙ベース請求書要否")

    def __str__(self):
        return f"{self.staff_last_name} {self.staff_first_name}"


class Project(models.Model):
    """案件を表すクラス
    """

    company = models.ForeignKey(CompanyBasicInfo, on_delete=models.CASCADE, related_name='project',
                                verbose_name="企業")

    name = models.CharField(max_length=20,
                            verbose_name="案件名")

    is_open = models.BooleanField(default=True,
                                  verbose_name="募集しているか")

    min_fee = models.IntegerField(verbose_name="最小単金")

    max_fee = models.IntegerField(verbose_name="最大単金")

    workplace = models.CharField(max_length=50,
                                 verbose_name="作業場所(住所/ビル名など)")

    closest_station = models.CharField(max_length=20,
                                       verbose_name="最寄り駅")

    start_term = models.DateField(verbose_name="開始時期(xxxx年mm月)")

    end_term = models.DateField(null=True, blank=True,
                                verbose_name="終了時間(xxxx年mm月)")

    start_time = models.TimeField(verbose_name="就業開始時間")

    end_time = models.TimeField(verbose_name="就業終了時間")

    rest_time = models.TimeField(verbose_name="就業中の休憩時間")

    garments = models.IntegerField(choices=GARMENTS_CHOICES, default=0,
                                   verbose_name="服装")

    restroom = models.IntegerField(choices=RESTROOM_CHOICES, default=0,
                                   verbose_name="トイレ")

    water_server = models.IntegerField(choices=USE_CHOICES, default=0,
                                       verbose_name="ウォーターサーバなどの利用")

    warter_supply_room = models.IntegerField(choices=USE_CHOICES, default=0,
                                             verbose_name="給湯室などの利用")

    conditions = models.CharField(max_length=50, null=True, blank=True,
                                  verbose_name="条件備考")

    content = models.TextField(verbose_name="作業内容")

    appeal = models.TextField(null=True, blank=True,
                              verbose_name="作業のアピール点")

    required_skills = models.TextField(null=True, blank=True,
                                       verbose_name="必須スキル")

    preferred_skills = models.TextField(null=True, blank=True,
                                        verbose_name="尚可スキル")

    def __str__(self):
        return f"{self.name}"
