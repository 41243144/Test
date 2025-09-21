from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from django.contrib.auth.models import Group
from wagtail import hooks
from django.urls import re_path
"""
class GroupAdmin(ModelAdmin):
    model = Group
    menu_label    = "群組管理"
    menu_icon     = "group"
    list_display  = ("name", "get_permissions")
    search_fields = ("name",)
    list_filter   = ("permissions",)

    def get_permissions(self, obj):
        # 顯示這個群組擁有的所有權限名稱
        return ", ".join(p.name for p in obj.permissions.all())
    get_permissions.short_description = "權限列表"

modeladmin_register(GroupAdmin)
"""

@hooks.register('construct_main_menu')
def hide_menu_items(request, menu_items):
    names_to_hide = {'settings', 'reports', 'help'}
    menu_items[:] = [
        item for item in menu_items
        if not (hasattr(item, 'name') and item.name in names_to_hide)
    ]
