from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_items', 'total_price', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    
    def total_items(self, obj):
        return obj.total_items
    total_items.short_description = '商品總數'
    
    def total_price(self, obj):
        return f"NT$ {obj.total_price:,.0f}"
    total_price.short_description = '總價格'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart_user', 'product', 'quantity', 'price', 'total_price_display', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('cart__user__email', 'product__name')
    readonly_fields = ('created_at', 'updated_at', 'total_price_display')
    
    def cart_user(self, obj):
        return obj.cart.user.email
    cart_user.short_description = '用戶'
    
    def total_price_display(self, obj):
        return f"NT$ {obj.total_price:,.0f}"
    total_price_display.short_description = '小計'
