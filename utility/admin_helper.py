
from django.urls import reverse


def get_model_link(model, label):
    """モデルへのリンクURLを返す

    Args:
        model (Model): ターゲットのModel
        label (str): 表示ラベル

    Returns:
        str: 表示用URL
    """

    url = reverse(
        f'admin:{model._meta.app_label}_{model._meta.model_name}_change', args=(model.pk,)
    )
    return f"<a href='{url}'>{label}<\a>"
