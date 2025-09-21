from django import template
from django.core.cache import cache
from wagtail.models import Site
from apps.home.models import SiteBasicSetting

register = template.Library()


def get_site_settings(request):
    """
    取得網站設定的輔助函數
    """
    site = Site.find_for_request(request)
    cache_key = f'site_basic_settings_{site.id}'
    settings = cache.get(cache_key)
    
    if settings is None:
        try:
            # 使用 Wagtail 的設定 API
            settings = SiteBasicSetting.for_request(request)
            if not settings:
                # 如果沒有設定，嘗試取得預設的第一筆記錄
                settings = SiteBasicSetting.objects.first()
            # 快取 5 分鐘
            cache.set(cache_key, settings, 300)
        except (SiteBasicSetting.DoesNotExist, AttributeError):
            settings = None
    
    return settings


@register.inclusion_tag('home/tags/site_settings.html', takes_context=True)
def site_basic_settings(context):
    """
    取得網站基本設定的模板標籤
    用法：{% site_basic_settings %}
    """
    request = context.get('request')
    settings = get_site_settings(request)
    
    return {
        'settings': settings,
        'request': request,
    }


@register.simple_tag(takes_context=True)
def get_site_setting(context, setting_name):
    """
    取得特定的網站設定值
    用法：{% get_site_setting 'site_name' %}
    """
    request = context.get('request')
    settings = get_site_settings(request)
    
    if settings and hasattr(settings, setting_name):
        return getattr(settings, setting_name)
    
    return ''


@register.simple_tag(takes_context=True)
def get_social_links(context):
    """
    取得社群媒體連結
    用法：{% get_social_links %}
    """
    request = context.get('request')
    settings = get_site_settings(request)
    
    if settings:
        return settings.get_social_links()
    
    return []


# 維護模式過濾器已移除


@register.inclusion_tag('home/tags/meta_tags.html', takes_context=True)
def render_meta_tags(context, title=None, description=None):
    """
    渲染 SEO meta 標籤
    用法：{% render_meta_tags %}
           {% render_meta_tags title="自訂標題" description="自訂描述" %}
    """
    request = context.get('request')
    settings = get_site_settings(request)
    
    # 使用自訂標題或預設標題
    meta_title = title or (settings.default_meta_title if settings else '尚虎雲平台')
    meta_description = description or (settings.default_meta_description if settings else '農業生產銷售一體化平台')
    
    return {
        'meta_title': meta_title,
        'meta_description': meta_description,
        'settings': settings,
        'request': request,
    }


@register.simple_tag
def google_analytics_code(ga_id=None):
    """
    產生 Google Analytics 程式碼
    用法：{% google_analytics_code %}
    """
    if not ga_id:
        return ''
    
    return f"""
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{ga_id}');
    </script>
    """


@register.simple_tag
def google_tag_manager_head(gtm_id=None):
    """
    產生 Google Tag Manager <head> 部分程式碼
    用法：{% google_tag_manager_head %}
    """
    if not gtm_id:
        return ''
    
    return f"""
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','{gtm_id}');</script>
    <!-- End Google Tag Manager -->
    """


@register.simple_tag
def google_tag_manager_body(gtm_id=None):
    """
    產生 Google Tag Manager <body> 部分程式碼
    用法：{% google_tag_manager_body %}
    """
    if not gtm_id:
        return ''
    
    return f"""
    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id={gtm_id}"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->
    """
