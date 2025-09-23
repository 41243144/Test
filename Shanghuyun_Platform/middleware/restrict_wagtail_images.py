from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.contrib.auth.views import redirect_to_login


class RestrictWagtailImagesAdminMiddleware:
    """
    限制只有超級管理員可以訪問 /admin/images/ 下的後台頁面
    但允許所有人使用 /admin/images/chooser/ (圖片選擇器)
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path  # 例如：/admin/images/、/admin/images/123/change/

        if path.startswith('/admin/images/') and 'chooser/' not in path:
            # 未登入者導到登入頁
            if not request.user.is_authenticated:
                return redirect_to_login(next=path, login_url=reverse('wagtailadmin_login'))

            # 非超管禁止
            if not request.user.is_superuser:
                raise PermissionDenied("只有超級管理員可以訪問圖片管理功能")

        return self.get_response(request)
