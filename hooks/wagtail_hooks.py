from .api_v1_account import *
from .api_v1_vendor import *
from .api_v1_product import *
from .api_v1_order import *
from .group import *
from .page import *
from .site_settings_hooks import *

from wagtail.admin.menu import MenuItem
from wagtail import hooks
from django.urls import reverse

# 載入你的 Setting model
from apps.users.models.privacy_policy import SitePolicySetting
from apps.users.models.terms_of_service import SiteTermsSetting

@hooks.register('construct_main_menu')
def add_homepage_link(request, menu_items):
    menu_items.append(
        MenuItem(
            label="回到首頁",
            url="/",
            icon_name="home",
            classname="custom-home-link",
            order=10000,
            attrs={"target": "_blank"}
        )
    )

@hooks.register('register_admin_menu_item')
def register_privacy_policy_menu_item():
    # 取出正確的 app_label 跟 model_name
    app_label  = SitePolicySetting._meta.app_label      # -> "users"
    model_name = SitePolicySetting._meta.model_name     # -> "sitepolicysetting"
    url = reverse('wagtailsettings:edit', args=[app_label, model_name])

    return MenuItem(
        '隱私權政策',           
        url,                   
        icon_name='doc-full-inverse',  
        order=300              
    )

@hooks.register('register_admin_menu_item')
def register_terms_of_service_menu_item():
    # 取出正確的 app_label 跟 model_name
    app_label  = SiteTermsSetting._meta.app_label      # -> "users"
    model_name = SiteTermsSetting._meta.model_name     # -> "sitetermssetting"
    url = reverse('wagtailsettings:edit', args=[app_label, model_name])

    return MenuItem(
        '服務條款',           
        url,                   
        icon_name='doc-full',  
        order=300              
    )


@hooks.register('construct_main_menu')
def rename_snippets_menu(request, menu_items):
    """將 Snippets 選單名稱改為 '分類'"""
    for item in menu_items:
        if hasattr(item, 'name') and item.name == 'snippets':
            item.label = '分類'
        elif hasattr(item, 'label') and item.label == 'Snippets':
            item.label = '分類'
