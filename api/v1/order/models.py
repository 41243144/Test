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
    merchant_trade_no = models.CharField(max_length=20, blank=True, unique=True)

    def save(self, *args, **kwargs):
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # 更新商品銷售統計
        self.product.update_sales_count()

    def delete(self, *args, **kwargs):
        product = self.product
        super().delete(*args, **kwargs)
        # 更新商品銷售統計
        product.update_sales_count()

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
