from wagtail_modeladmin.helpers import PermissionHelper
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from allauth.account.models import EmailAddress
from api.v1.account.models import User, Profile
from django.contrib.auth.models import Group
from wagtail import hooks
from django.urls import re_path
from django.template.response import TemplateResponse

class SuperuserOnlyPermissionHelper(PermissionHelper):
    def user_can_list(self, user):
        return user.is_superuser
    def user_can_create(self, user):
        return user.is_superuser
    def user_can_edit(self, user):
        return user.is_superuser
    def user_can_delete(self, user):
        return user.is_superuser

class UserAdmin(ModelAdmin):
    model = User
    menu_label = '用戶管理'
    menu_icon = 'user'
    permission_helper_class = SuperuserOnlyPermissionHelper
    list_display = ('email', 'email_verified', 'is_active', 'is_staff')
    search_fields = ('email',)
    form_fields = [
        'username', 'email', 'is_active', 'is_staff', 
    ]
    form_fields_exclude = [
        'password', 'groups', 'user_permissions',
    ]

    def email_verified(self, obj):
        return EmailAddress.objects.filter(
            user=obj,
            email=obj.email,
            verified=True
        ).exists()
    email_verified.boolean = True
    email_verified.short_description = '信箱已驗證'

modeladmin_register(UserAdmin)

class ProfileAdmin(ModelAdmin):
    model = Profile
    menu_label = '個人檔案'
    menu_icon = 'form'
    permission_helper_class = SuperuserOnlyPermissionHelper
    list_display = ('user', 'portrait', 'real_name', 'nickname', 'address', 'phone')
    search_fields = ('user__username', 'email', 'real_name')
modeladmin_register(ProfileAdmin)

@hooks.register('register_admin_urls')
def hide_users_admin_urls():
    def users_not_found(request, *args, **kwargs):
        return TemplateResponse(request, 'wagtailadmin/404.html', status=404)

    return [
        # hide all /admin/users/
        re_path(
            r"^users/.*$",
            users_not_found,
            name="hide_wagtail_users"
        ),
    ]
