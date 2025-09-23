from django import template
import re
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def mul(value, arg):
    """
    乘法過濾器，將兩個數值相乘
    用法：{{ value|mul:arg }}
    """
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def div(value, arg):
    """
    除法過濾器，將兩個數值相除
    用法：{{ value|div:arg }}
    """
    try:
        arg = int(arg)
        if arg == 0:
            return 0
        return int(value) / arg
    except (ValueError, TypeError):
        return 0


@register.filter
def mod(value, arg):
    """
    取餘數過濾器
    用法：{{ value|mod:arg }}
    """
    try:
        arg = int(arg)
        if arg == 0:
            return 0
        return int(value) % arg
    except (ValueError, TypeError):
        return 0


@register.filter
def subtract(value, arg):
    """
    減法過濾器，從 value 減去 arg
    用法：{{ value|subtract:arg }}
    """
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def safe_iframe(value):
    """
    安全地輸出 iframe 代碼
    用法：{{ iframe_code|safe_iframe }}
    """
    if not value:
        return ''
    
    # 基本的安全檢查，確保只包含 iframe 標籤
    if '<iframe' in value.lower() and '</iframe>' in value.lower():
        return mark_safe(value)
    else:
        return ''


@register.filter
def extract_iframe_src(value):
    """
    從 iframe 代碼中提取 src 屬性
    用法：{{ iframe_code|extract_iframe_src }}
    """
    if not value:
        return ''
    
    # 使用正則表達式提取 src 屬性
    pattern = r'<iframe[^>]*src=["\']([^"\']*)["\'][^>]*>'
    match = re.search(pattern, value, re.IGNORECASE)
    
    if match:
        return match.group(1)
    else:
        return ''
