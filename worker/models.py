from django.db import models
from django.utils import timezone

from certification.models import User

WORKING_STATUS_CHOICES = (
    (0, 'now'),
    (1, 'after 1week'),
    (2, 'after 2week'),
    (3, 'after 1month'),
    (4, 'after 3month'),
)

WORK_STYLE_CHOICES = (
    (0, '1day'),
    (1, '2days'),
    (2, '3days'),
    (3, '4days'),
    (4, '5days'),
)


class Worker(models.Model):
    """ユーザの一般情報を管理するクラス
    """
    account = models.OneToOneField(User, on_delete=models.CASCADE, related_name='worker',
                                   verbose_name="Workerのアカウント", null=True, blank=True, unique=True)

    is_activate = models.BooleanField(default=False,
                                      verbose_name="入力が完了したか否か")

    last_name = models.CharField(max_length=16, null=True, blank=True,
                                 verbose_name="氏")

    first_name = models.CharField(max_length=16, null=True, blank=True,
                                  verbose_name="名")

    working_status = models.CharField(max_length=16, null=True, blank=True,
                                      verbose_name="稼働中か否か")

    work_style = models.IntegerField(choices=WORK_STYLE_CHOICES, null=True, blank=True,
                                     verbose_name="稼働可能日数(ex. 週xx日〜)")

    hope_fee = models.IntegerField(null=True, blank=True,
                                   verbose_name="希望する単金")

    open_status = models.IntegerField(choices=WORKING_STATUS_CHOICES, null=True, blank=True,
                                      verbose_name="働けるか否か")

    interested_work = models.TextField(null=True, blank=True,
                                       verbose_name="興味のある業種")

    qiita_url = models.URLField(null=True, blank=True,
                                verbose_name="QiitaのURL")

    github_url = models.URLField(null=True, blank=True,
                                 verbose_name="GithubのURL")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class WorkerBank(models.Model):
    """ユーザの銀行口座情報
    """
    worker = models.OneToOneField(Worker, on_delete=models.CASCADE, related_name='bank',
                                  verbose_name="対応ユーザ", null=False, blank=False)

    is_activate = models.BooleanField(default=False,
                                      verbose_name="入力が完了したか否か")

    name = models.CharField(max_length=50, null=True, blank=True,
                            verbose_name="銀行名")

    office_code = models.CharField(max_length=50, null=True, blank=True,
                                   verbose_name="銀行支店コード")

    account_type = models.CharField(max_length=50, null=True, blank=True,
                                    verbose_name="口座種類")

    account_number = models.CharField(max_length=16, null=True, blank=True,
                                      verbose_name="口座番号")

    def __str__(self):
        return f"{self.name}"


class Resume(models.Model):
    """ユーザの経験情報を管理するクラス
    """
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='resumes',
                               verbose_name="対応ユーザ")

    project_name = models.CharField(max_length=50,
                                    verbose_name="プロジェクト名")

    started_at = models.DateField(verbose_name="開始年月")

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
