from wagtail_modeladmin.options import ModelAdmin, modeladmin_register 
from api.v1.order.models import Order

class OrderAdmin(ModelAdmin):
    model = Order
    menu_label = "Orders"
    menu_icon = "list-ul"  # FontAwesome icon
    list_display = ("id", "user", "total_amount", "status", "created_at")
    search_fields = ("id", "user__username")
modeladmin_register(OrderAdmin)
