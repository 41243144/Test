from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtail_modeladmin.helpers import PermissionHelper
from api.v1.order.models import Order


class OrderPermissionHelper(PermissionHelper):
    """放寬清單查看權限，但限制新增/刪除/編輯僅限管理員與員工。"""

    def user_can_list(self, user):
        # 已登入者可看到清單（實際資料在 get_queryset 過濾）
        return user.is_authenticated

    def user_can_create(self, user):
        return user.is_superuser or user.is_staff

    def user_can_delete_obj(self, user, obj):
        return user.is_superuser or user.is_staff

    def user_can_edit_obj(self, user, obj):
        return user.is_superuser or user.is_staff

class OrderAdmin(ModelAdmin):
    model = Order
    menu_label = "訂單管理"
    menu_icon = "list-ul"  # FontAwesome icon
    list_display = ("id", "user", "total_amount", "status", "created_at")
    search_fields = ("id", "user__email", "user__username")
    permission_helper_class = OrderPermissionHelper

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # 僅顯示已付款訂單
        qs = qs.filter(status="paid")

        # 管理員/員工可見全部已付款訂單
        if request.user.is_superuser or request.user.is_staff:
            return qs

        # 商家僅能看到含有自己商品的訂單
        # Order -> OrderItem (related_name="items") -> Product -> Vendor -> User
        return qs.filter(items__product__vendor__user=request.user).distinct()

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_edit_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff


modeladmin_register(OrderAdmin)
