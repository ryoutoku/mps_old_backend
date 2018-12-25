from django.db import models


class User(models.Model):
    """ユーザの一般情報を管理するクラス

    last_name       : 氏
    fist_name       : 名
    mail_address    : メールアドレス
    working_status  : 稼働中か否か
    work_style      : 稼働可能日数(ex. 週xx日〜)
    hope_fee        : 希望する単金
    open_status     : 働けるか否か
    interested_work : 興味のある業種

    bank_company        : 銀行名
    bank_office_code    : 銀行支店コード
    bank_account_type   : 口座種類
    bank_account_number : 口座番号

    joined_date                 : 入会年月日
    defected_date               : 退会年月日
    """

    last_name = models.CharField(max_length=16)
    fist_name = models.CharField(max_length=16)
    mail_address = models.EmailField()
    working_status = models.CharField(max_length=16)
    work_style = models.CharField(max_length=16)
    hope_fee = models.IntegerField()
    open_status = models.CharField()
    interested_work = models.TextField()

    bank_company = models.CharField(max_length=50)
    bank_office_code = models.CharField(max_length=50)
    bank_account_type = models.CharField(max_length=50)
    bank_account_number = models.CharField()

    joined_date = models.DateTimeField(default=timezone.now)
    defected_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(name)


class Career(models.Model):
    """ユーザの経験情報を管理するクラス

    project_name    : プロジェクト名
    started_at      : 開始年月
    ended_at        : 終了年月
    position        : プロジェクトでのポジション
    scale           : 開発規模
    tools           : 開発ツール、フレームワークなど
    details         : 詳細
    """
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='career')

    project_name = models.CharField(max_length=50)
    started_at = models.DateField()
    ended_at = models.DateField(null=True, blank=True)
    position = models.CharField()
    scale = models.CharField()
    tools = models.CharField()
    details = models.TextField()

    class Meta:
        ordering = ("start_at")

    def __str__(self):
        return str(project_name)
