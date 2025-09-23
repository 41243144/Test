from wagtail.admin.menu import MenuItem
from wagtail import hooks
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied

# 載入網站基本設定模型
from apps.home.models import SiteBasicSetting
from apps.users.models.privacy_policy import SitePolicySetting
from apps.users.models.terms_of_service import SiteTermsSetting


@hooks.register('register_admin_menu_item')
def register_site_basic_setting_menu_item():
    """
    註冊網站基本設定選單項目
    只有超級管理員可以看到此選單
    """
    # 取出正確的 app_label 跟 model_name
    app_label = SiteBasicSetting._meta.app_label      # -> "home"
    model_name = SiteBasicSetting._meta.model_name    # -> "sitebasicsetting"
    url = reverse('wagtailsettings:edit', args=[app_label, model_name])

    return MenuItem(
        '網站基本設定',           
        url,                   
        icon_name='cogs',  
        order=100,              # 設定較高的優先級
        classname='icon icon-cogs',
    attrs={'title': '僅限超級管理員'}
    )

@hooks.register('construct_main_menu')
def hide_site_settings_for_non_superusers(request, menu_items):
    """
    確保非超級管理員無法看到網站設定相關選單
    """
    if not request.user.is_superuser:
        # 移除任何可能的網站設定選單項目
        menu_items_to_remove = []
        for item in menu_items:
            if hasattr(item, 'label') and ('網站基本設定' in item.label or '隱私權政策' in item.label or '服務條款' in item.label):
                menu_items_to_remove.append(item)
        
        for item in menu_items_to_remove:
            menu_items.remove(item)

# @hooks.register('register_admin_urls')
# def restrict_images_admin_urls():
#     """
#     限制只有超級管理員可以訪問 Images 管理後台 (非選擇器)
#     但允許一般用戶使用圖片選擇器 (chooser)
#     """
#     from django.urls import re_path
    
#     def check_superuser_permission(request, *args, **kwargs):
#         if not request.user.is_superuser:
#             raise PermissionDenied("只有超級管理員可以訪問圖片管理功能")
#         return None

#     return [
#         # 只限制管理界面，不限制選擇器
#         re_path(
#             r"^images/(?!chooser/).*$",  # 不匹配 chooser/ 路徑
#             check_superuser_permission,
#             name="restrict_wagtail_images_admin"
#         ),
#     ]

@hooks.register('before_edit_snippet')
def check_site_settings_permissions(request, instance):
    """
    檢查編輯網站設定的權限
    只有超級管理員可以編輯
    """
    if isinstance(instance, (SiteBasicSetting, SitePolicySetting, SiteTermsSetting)):
        if not request.user.is_superuser:
            from django.core.exceptions import PermissionDenied
            model_name = instance._meta.verbose_name
            raise PermissionDenied(f"只有超級管理員可以編輯{model_name}")


@hooks.register('before_create_snippet')
def check_site_settings_create_permissions(request, model):
    """
    檢查創建網站設定的權限
    只有超級管理員可以創建
    """
    if model in [SiteBasicSetting, SitePolicySetting, SiteTermsSetting]:
        if not request.user.is_superuser:
            from django.core.exceptions import PermissionDenied
            model_name = model._meta.verbose_name
            raise PermissionDenied(f"只有超級管理員可以創建{model_name}")


@hooks.register('register_permissions')
def register_site_settings_permissions():
    """
    註冊網站設定的自訂權限
    """
    permissions = []
    
    # 註冊網站基本設定權限
    basic_content_type = ContentType.objects.get_for_model(SiteBasicSetting)
    permissions.extend(Permission.objects.filter(
        content_type=basic_content_type,
        codename__in=['can_edit_site_settings']
    ))
    
    # 註冊隱私權政策權限
    policy_content_type = ContentType.objects.get_for_model(SitePolicySetting)
    permissions.extend(Permission.objects.filter(
        content_type=policy_content_type,
        codename__in=['can_edit_privacy_policy']
    ))
    
    # 註冊服務條款權限
    terms_content_type = ContentType.objects.get_for_model(SiteTermsSetting)
    permissions.extend(Permission.objects.filter(
        content_type=terms_content_type,
        codename__in=['can_edit_terms_of_service']
    ))
    
    return permissions


def is_vendor_user(user):
    """檢查使用者是否為商家"""
    return hasattr(user, 'vendor_profile') or getattr(user, 'is_vendor', False)


@hooks.register('before_edit_page')
def check_vendor_page_edit_permissions(request, page):
    """
    限制商家用戶編輯頁面
    商家只能新增商品，不能修改頁面
    """
    if is_vendor_user(request.user) and not request.user.is_superuser:
        raise PermissionDenied("商家用戶不能編輯頁面，請使用商品管理功能")


@hooks.register('before_create_page')
def check_vendor_page_create_permissions(request, parent_page, page_class):
    """
    限制商家用戶創建頁面
    商家只能新增商品，不能創建頁面
    """
    if is_vendor_user(request.user) and not request.user.is_superuser:
        raise PermissionDenied("商家用戶不能創建頁面，請使用商品管理功能新增商品")


@hooks.register('before_delete_page')
def check_vendor_page_delete_permissions(request, page):
    """
    限制商家用戶刪除頁面
    """
    if is_vendor_user(request.user) and not request.user.is_superuser:
        raise PermissionDenied("商家用戶不能刪除頁面")


@hooks.register('construct_main_menu')
def hide_pages_menu_for_vendors(request, menu_items):
    """
    為商家用戶隱藏頁面相關選單項目
    但允許使用圖片選擇器功能
    """
    if is_vendor_user(request.user) and not request.user.is_superuser:
        # 需要隱藏的選單項目名稱 (移除 'images' 以允許圖片選擇器功能)
        items_to_hide = ['pages', 'documents', 'snippets', 'forms']
        
        menu_items_to_remove = []
        for item in menu_items:
            if hasattr(item, 'name') and item.name in items_to_hide:
                menu_items_to_remove.append(item)
            elif hasattr(item, 'label') and ('頁面' in item.label or '文件' in item.label):
                menu_items_to_remove.append(item)
            # 隱藏圖片管理選單項目，但不阻止圖片選擇器功能
            elif hasattr(item, 'name') and item.name == 'images':
                menu_items_to_remove.append(item)
        
        for item in menu_items_to_remove:
            menu_items.remove(item)
