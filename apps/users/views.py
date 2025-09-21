# apps/users/views.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from apps.users.models.privacy_policy import SitePolicySetting
from apps.users.models.terms_of_service import SiteTermsSetting

def is_superuser(user):
    """檢查使用者是否為超級管理員"""
    return user.is_authenticated and user.is_superuser

class ProfilePageView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile_page.html'
    login_url = reverse_lazy('account_login')  # 未登入時導向的 URL，這裡使用 allauth 的登入 URL

@user_passes_test(is_superuser, login_url='account_login')
def privacy_policy(request):
    """
    隱私權政策頁面 - 僅限超級管理員訪問
    """
    # load() 会根据当前站点（或所有站点）拿到唯一的那条设置
    site_policy = SitePolicySetting.load(request_or_site=request)
    return render(request, "users/privacy_policy.html", {
        "site_policy": site_policy,
    })

@user_passes_test(is_superuser, login_url='account_login')
def terms_of_service(request):
    """
    服務條款頁面 - 僅限超級管理員訪問
    """
    # load() 会根据当前站点（或所有站点）拿到唯一的那条设置
    site_terms = SiteTermsSetting.load(request_or_site=request)
    return render(request, "users/terms_of_service_page.html", {
        "site_terms": site_terms,
    })