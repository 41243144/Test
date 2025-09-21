from django.apps import AppConfig
from django.db.models.signals import post_migrate


class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.home"

    def ready(self):
        from .signals import ensure_homepage  # 匯入 signal handler
        # 只在本 app 的 migrations 跑完後觸發，避免多 app 重複執行
        post_migrate.connect(ensure_homepage, sender=self)