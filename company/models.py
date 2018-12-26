from django.db import models
from django.utils import timezone


class Company(models.Model):
    """企業の経験情報を管理するクラス

    name                        : 企業名
    staff_name                  : 担当者名
    phone_number                : 電話番号
    mail_address                : メールアドレス
    address                     : 企業住所
    closest_station_1           : 最寄り駅1
    closest_station_2           : 最寄り駅2
    needs_paper_invoice         : 紙ベース請求書要否
    company_url                 : 企業のコーポレートURL
    start_office_hours          : 就業の開始時間
    end_office_hours            : 就業の終了時間
    invoice_staff               : 請求書宛先担当者
    invoice_staff_mail_address  : 請求書宛先メールアドレス
    pr_comment                  : 企業のPRコメント
    pr_photo_1                  : 企業のPR写真1
    pr_photo_2                  : 企業のPR写真2

    joined_date                 : 入会年月日
    defected_date               : 退会年月日
    """

    name = models.CharField(max_length=50)
    staff_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    mail_address = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    closest_station_1 = models.CharField(max_length=50)
    closest_station_2 = models.CharField(max_length=50)
    needs_paper_invoice = models.BooleanField(default=False)
    company_url = models.URLField()
    start_office_hours = models.TimeField()
    end_office_hours = models.TimeField()
    contact_staff = models.CharField(max_length=50)
    contact_staff_mail_address = models.CharField(max_length=50)
    pr_comment = models.TextField()
    pr_photo_1 = models.ImageField(upload_to='uploads/company/image')
    pr_photo_2 = models.ImageField(upload_to='uploads/company/image')

    joined_date = models.DateTimeField(default=timezone.now)
    defected_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(name)


class Project(models.Model):
    """案件を表すクラス
    name                : 案件名
    min_fee             : 最小単金
    max_fee             : 最大単金
    workplace           : 作業場所(住所/ビル名など)
    closest_station     : 最寄り駅
    start_term          : 開始時期(xxxx年mm月)
    end_term            : 終了時間(xxxx年mm月)
    start_time          : 就業開始時間
    end_time            : 就業終了時間
    rest_tim            : 就業中の休憩時間

    garments            : 服装
    restroom            : トイレ
    conditions          : 条件備考

    content             : 作業内容
    appeal              : 作業のアピール点

    required_skills     : 必須スキル
    preferred_skills    : 尚可スキル
    """

    name = models.CharField(max_length=16)
    min_fee = models.IntegerField()
    max_fee = models.IntegerField()
    workplace = models.CharField(max_length=16)
    closest_station = models.CharField(max_length=50)
    start_term = models.DateField(),
    end_term = models.DateField(null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    rest_time = models.TimeField()

    garments = models.CharField(max_length=16, null=True, blank=True)
    restroom = models.CharField(max_length=16, null=True, blank=True)
    conditions = models.CharField(max_length=16, null=True, blank=True)

    content = models.TextField()
    appeal = models.TextField()

    required_skills = models.TextField(null=True, blank=True)
    preferred_skills = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(name)
