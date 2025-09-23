from django.db import models
from api.v1.product.models import Product
from api.v1.account.models import User
import uuid

class Order(models.Model):
    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_FAILED = "failed"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default=STATUS_PENDING)  # pending / paid / failed
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)  # 付款時間
    merchant_trade_no = models.CharField(max_length=20, blank=True, unique=True)

    def get_total_items_count(self):
        """獲取訂單中商品總數量"""
        return sum(item.quantity for item in self.items.all())
    
    def recalculate_total(self):
        """重新計算訂單總金額"""
        total = sum(item.get_total() for item in self.items.all())
        self.total_amount = total
        return total

    def update_status(self, new_status):
        """更新訂單狀態並處理相關邏輯"""
        old_status = self.status
        self.status = new_status
        
        # 如果從未付款狀態變為已付款，更新商品銷售統計
        if old_status != self.STATUS_PAID and new_status == self.STATUS_PAID:
            for item in self.items.all():
                item.product.update_sales_count()
        
        # 如果從已付款狀態變為其他狀態，需要重新計算銷售統計
        elif old_status == self.STATUS_PAID and new_status != self.STATUS_PAID:
            for item in self.items.all():
                item.product.update_sales_count()
        
        self.save()

    def save(self, *args, **kwargs):
        # 檢查狀態是否有變更
        if self.pk:  # 如果是更新現有訂單
            old_order = Order.objects.filter(pk=self.pk).first()
            if old_order and old_order.status != self.status:
                # 狀態有變更，處理銷售統計
                if old_order.status != self.STATUS_PAID and self.status == self.STATUS_PAID:
                    # 從未付款變為已付款，設置付款時間並增加銷售統計
                    from django.utils import timezone
                    if not self.paid_at:
                        self.paid_at = timezone.now()
                    super().save(*args, **kwargs)  # 先保存訂單狀態
                    for item in self.items.all():
                        item.product.update_sales_count()
                    return
                elif old_order.status == self.STATUS_PAID and self.status != self.STATUS_PAID:
                    # 從已付款變為其他狀態，清除付款時間並重新計算銷售統計
                    self.paid_at = None
                    super().save(*args, **kwargs)
                    for item in self.items.all():
                        item.product.update_sales_count()
                    return
        
        # 如果還沒有 merchant_trade_no，先存一次產生 id
        if not self.merchant_trade_no:
            super().save(*args, **kwargs)  # 先存一次，產生 self.id
            self.merchant_trade_no = f"{self.id}{uuid.uuid4().hex[:6].upper()}"
            kwargs['force_insert'] = False  # 避免重複插入
        super().save(*args, **kwargs)  # 再存一次更新 merchant_trade_no
        
    def __str__(self):
        return f"Order {self.id} by {self.user.email}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total(self):
        """計算該項目的總價 (數量 x 單價)"""
        return self.quantity * self.price

    @property
    def total(self):
        """總價的屬性方式訪問"""
        return self.get_total()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # 移除自動更新銷售統計 - 應該在付款完成後才計算
        # self.product.update_sales_count()

    def delete(self, *args, **kwargs):
        product = self.product
        super().delete(*args, **kwargs)
        # 如果該訂單已付款，需要減少銷售統計
        if self.order.status == Order.STATUS_PAID:
            product.update_sales_count()

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
