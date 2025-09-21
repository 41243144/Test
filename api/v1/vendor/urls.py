from django.urls import path
from . import views

app_name = "vendor"

urlpatterns = [
    # 暫定提供一個健康檢查端點，確認路由與 app 正常
    path("health/", views.health, name="health"),
]
