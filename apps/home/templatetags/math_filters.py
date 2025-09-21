from django import template

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
