from django.db import models
from django.utils import timezone


class User(models.Model):
    """ユーザの一般情報を管理するクラス
    """
    WORKING_STATUS_CHOICES=(
        (0, 'now'),
        (1, 'after 1week'),
        (2, 'after 2week'),
        (3, 'after 1month'),
        (4, 'after 3month'),
    )

    WORK_STYLE_CHOICES=(
        (0, '1day'),
        (1, '2days'),
        (2, '3days'),
        (3, '4days'),
        (4, '5days'),
        )

    last_name = models.CharField(max_length=16,
        verbose_name="氏")
    first_name = models.CharField(max_length=16,
        verbose_name="名")
    mail_address = models.EmailField(
        verbose_name="メールアドレス")
    working_status = models.CharField(max_length=16,
        verbose_name="稼働中か否か")
    work_style = models.CharField(max_length=16, choices=WORK_STYLE_CHOICES,
        verbose_name="稼働可能日数(ex. 週xx日〜)")
    hope_fee = models.IntegerField(
        verbose_name="希望する単金")
    open_status = models.CharField(max_length=16, choices=WORKING_STATUS_CHOICES,
        verbose_name="働けるか否か")
    interested_work = models.TextField(
        verbose_name="興味のある業種")
    qiita_url = models.URLField(null=True, blank=True,
        verbose_name="QiitaのURL")
    github_url = models.URLField(null=True, blank=True,
        verbose_name="GithubのURL")
    joined_date = models.DateTimeField(default=timezone.now,
        verbose_name="入会年月日")
    defected_date = models.DateField(null=True, blank=True, 
        verbose_name="退会年月日")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class UserBank(models.Model):
    """ユーザの銀行口座情報
    """
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='bank',
        verbose_name="対応ユーザ")
    name = models.CharField(max_length=50,
        verbose_name="銀行名")
    office_code = models.CharField(max_length=50,
        verbose_name="銀行支店コード")
    account_type = models.CharField(max_length=50,
        verbose_name="口座種類")
    account_number = models.CharField(max_length=16,
        verbose_name="口座番号")

    def __str__(self):
        return f"{self.name}"


class Career(models.Model):
    """ユーザの経験情報を管理するクラス
    """
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='career',
        verbose_name="対応ユーザ")

    project_name = models.CharField(max_length=50,
        verbose_name="プロジェクト名")
    started_at = models.DateField(
        verbose_name="開始年月")
    ended_at = models.DateField(null=True, blank=True,
        verbose_name="終了年月")
    position = models.CharField(max_length=16,
        verbose_name="プロジェクトでのポジション")
    scale = models.CharField(max_length=16,
        verbose_name="開発規模")
    tools = models.CharField(max_length=16,
        verbose_name="開発ツール、フレームワークなど")
    details = models.TextField(
        verbose_name="プロジェクト詳細")

    class Meta:
        ordering = ("started_at", )

    def __str__(self):
        return str(self.project_name)
