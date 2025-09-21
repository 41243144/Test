from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtail_modeladmin.views import EditView
from wagtail_modeladmin.helpers import PermissionHelper
from django.core.exceptions import PermissionDenied
from api.v1.vendor.models import Vendor

class VendorEditView(EditView):
    """自訂編輯視圖，於視圖層處理權限與唯讀欄位。"""

    ALLOWED_FIELDS_FOR_VENDOR = {"intro", "description"}

    def get_form(self):
        form = super().get_form()
        user = self.request.user
        # 僅在非管理員/員工時限制欄位
        if not (user.is_superuser or user.is_staff):
            obj = getattr(form, "instance", None)
            if not obj or obj.user_id != user.id:
                raise PermissionDenied("您沒有權限編輯此商家資訊。")

            for name, field in form.fields.items():
                if name not in self.ALLOWED_FIELDS_FOR_VENDOR:
                    field.disabled = True
                    field.required = False
                    help_suffix = "（唯讀）"
                    if field.help_text:
                        if help_suffix not in str(field.help_text):
                            field.help_text = f"{field.help_text} {help_suffix}"
                    else:
                        field.help_text = help_suffix
        return form

    def form_valid(self, form):
        user = self.request.user
        if not (user.is_superuser or user.is_staff):
            obj = getattr(form, "instance", None)
            if not obj or obj.user_id != user.id:
                raise PermissionDenied("您沒有權限編輯此商家資訊。")

            # 嚴格限制：只允許 intro 變更，其他欄位回填原值
            for field_name in form.fields.keys():
                if field_name not in self.ALLOWED_FIELDS_FOR_VENDOR:
                    setattr(form.instance, field_name, getattr(obj, field_name))

        return super().form_valid(form)


class VendorPermissionHelper(PermissionHelper):
    """
    放寬權限：
    - 商家可看到清單（僅自己的資料），並可編輯自己的 Vendor（受表單限制）
    - 只有管理員/員工可以新增與刪除
    """

    def user_can_list(self, user):
        # 允許所有已登入者進入清單；實際資料由 get_queryset 過濾
        return user.is_authenticated

    def user_can_create(self, user):
        return user.is_superuser or user.is_staff

    def user_can_delete_obj(self, user, obj):
        return user.is_superuser or user.is_staff

    def user_can_edit_obj(self, user, obj):
        if user.is_superuser or user.is_staff:
            return True
        return obj and obj.user_id == user.id

    def user_can_inspect_obj(self, user, obj):
        # 停用 inspect 按鈕，避免未註冊 inspect 路由時發生 NoReverseMatch
        return False


class VendorAdmin(ModelAdmin):
    model = Vendor
    menu_label = "商家管理"         # 左側選單顯示文字
    menu_icon = "user"             # Wagtail icon name
    list_display = ("name", "user", "intro", "description", "address", "phone")
    search_fields = ("name", "user__email")

    # 使用自訂編輯視圖（不覆寫表單 class）
    edit_view_class = VendorEditView
    permission_helper_class = VendorPermissionHelper
    inspect_view_enabled = False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # 管理員/員工可見全部，商家僅能看到自己
        if request.user.is_superuser or request.user.is_staff:
            return qs
        return qs.filter(user=request.user)

    def has_add_permission(self, request):
        # 只有管理員/員工可以新增商家
        return request.user.is_superuser or request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        # 只有管理員/員工可以刪除商家
        return request.user.is_superuser or request.user.is_staff


modeladmin_register(VendorAdmin)
