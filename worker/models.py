from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

from certification.models import User

WORKING_STATUS_CHOICES = (
    (0, '---未登録---'),
    (1, '1月から'),
    (2, '2月から'),
    (3, '3月から'),
    (4, '4月から'),
    (5, '5月から'),
    (6, '6月から'),
    (7, '7月から'),
    (8, '8月から'),
    (9, '9月から'),
    (10, '10月から'),
    (11, '11月から'),
    (12, '12月から'),
)

WORK_STYLE_CHOICES = (
    (0, '---未登録---'),
    (1, '週1日'),
    (2, '週2日'),
    (3, '週3日'),
    (4, '週4日'),
    (5, '週5日'),
)

ACCOUNT_TYPE_CHOICES = {
    (0, '---未登録---'),
    (1, '普通預金'),
    (2, '当座預金')
}

SEX_TYPE_CHOICES = {
    (0, '---未登録---'),
    (1, '男性'),
    (2, '女性')
}

PROJECT_SCALE_CHOICES = {
    (0, '---未登録---'),
    (1, '~5人'),
    (2, '6~10人'),
    (3, '11~20人'),
    (4, '21~40人'),
    (5, '41人~'),
}


class WorkerBasicInfo(models.Model):
    """workerの一般情報を管理するクラス
    """

    phone_number_regex = RegexValidator(regex=r'^[0-9]+$', message=(
        "Tel Number must be entered in the format: '09012345678'. Up to 15 digits allowed."))

    account = models.OneToOneField(User, on_delete=models.CASCADE, related_name='worker',
                                   verbose_name="Workerのアカウント", unique=True)

    is_activated = models.BooleanField(default=False,
                                       verbose_name="必須入力が完了したか否か")

    last_name = models.CharField(max_length=10, null=True, blank=True,
                                 verbose_name="姓")

    last_name_kana = models.CharField(max_length=10, null=True, blank=True,
                                      verbose_name="セイ")

    first_name = models.CharField(max_length=10, null=True, blank=True,
                                  verbose_name="名")

    first_name_kana = models.CharField(max_length=10, null=True, blank=True,
                                       verbose_name="メイ")

    address = models.CharField(max_length=50, null=True, blank=True,
                               verbose_name="住所")

    phone_number = models.CharField(validators=[phone_number_regex], max_length=15, null=True, blank=True,
                                    verbose_name='電話番号')

    birth_day = models.DateField(null=True, blank=True,
                                 verbose_name="生年月日")

    sex = models.IntegerField(choices=SEX_TYPE_CHOICES, null=True, blank=True, default=0,
                              verbose_name="性別")

    bank_name = models.CharField(max_length=50, null=True, blank=True,
                                 verbose_name="銀行名")

    bank_office_code = models.CharField(max_length=5, null=True, blank=True,
                                        verbose_name="銀行支店コード")

    bank_account_type = models.IntegerField(choices=ACCOUNT_TYPE_CHOICES, null=True, blank=True, default=0,
                                            verbose_name="口座種類")

    bank_account_number = models.CharField(max_length=16, null=True, blank=True,
                                           verbose_name="口座番号")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Technology(models.Model):
    """技術領域
    """
    name = models.CharField(max_length=20,
                            verbose_name="技術力域の表示用フィールド")

    lower_name = models.CharField(max_length=20,
                                  verbose_name="技術力域の検索用フィールド(lower_caseで保存)")

    def __str__(self):
        return str(self.name)


class WorkerCondition(models.Model):
    """workerの希望条件などを管理するクラス
    """
    worker = models.OneToOneField(WorkerBasicInfo, on_delete=models.CASCADE, related_name='condition',
                                  verbose_name="Workerのアカウント", unique=True)

    is_open = models.BooleanField(default=False,
                                  verbose_name="公開するか否か")

    work_style = models.IntegerField(choices=WORK_STYLE_CHOICES, null=True, blank=True, default=0,
                                     verbose_name="稼働可能日数(ex. 週xx日〜)")

    hope_fee = models.IntegerField(null=True, blank=True,
                                   verbose_name="希望する単金")

    working_status = models.IntegerField(choices=WORKING_STATUS_CHOICES, null=True, blank=True, default=0,
                                         verbose_name="稼働開始可能月")

    interested_work = models.ManyToManyField(Technology, blank=True,
                                             verbose_name="興味のある業種")

    qiita_url = models.URLField(null=True, blank=True,
                                verbose_name="QiitaのURL")

    github_url = models.URLField(null=True, blank=True,
                                 verbose_name="GithubのURL")

    other_url = models.URLField(null=True, blank=True,
                                verbose_name="その他のURL")

    experience = models.IntegerField(null=True, blank=True, default=0,
                                     verbose_name="経験年数(単位:月)")

    def __str__(self):
        return f"{self.worker}"


class ProjectType(models.Model):
    project_type = models.CharField(max_length=20,
                                    verbose_name="プロジェクトの種類")

    def __str__(self):
        return str(self.project_type)


class ChargeOfProcess(models.Model):
    process_name = models.CharField(max_length=20,
                                    verbose_name="担当工程")

    def __str__(self):
        return str(self.process_name)


class RoleInProject(models.Model):

    role_name = models.CharField(max_length=20,
                                 verbose_name="役割")

    def __str__(self):
        return str(self.role_name)


class Resume(models.Model):
    """ユーザの経験情報を管理するクラス
    """
    worker = models.ForeignKey(WorkerBasicInfo, on_delete=models.CASCADE, related_name='resumes',
                               verbose_name="対応ユーザ")

    project_name = models.CharField(max_length=50,
                                    verbose_name="プロジェクト名")

    started_at = models.DateField(verbose_name="開始年月")

    ended_at = models.DateField(null=True, blank=True,
                                verbose_name="終了年月")

    project_type = models.ManyToManyField(ProjectType, blank=True,
                                          verbose_name="プロジェクトの種類")

    charge_of_process = models.ManyToManyField(ChargeOfProcess, blank=True,
                                               verbose_name="担当工程")

    role_in_project = models.ManyToManyField(RoleInProject, blank=True,
                                             verbose_name="プロジェクトでの役割")

    project_scale = models.IntegerField(choices=PROJECT_SCALE_CHOICES, null=True, blank=True, default=0,
                                        verbose_name="稼働可能日数(ex. 週xx日〜)")

    tools = models.ManyToManyField(Technology, blank=True,
                                   verbose_name="開発ツール、フレームワークなど")

    detail = models.TextField(
        verbose_name="プロジェクト詳細")

    class Meta:
        ordering = ("started_at", )

    def __str__(self):
        return str(self.project_name)
