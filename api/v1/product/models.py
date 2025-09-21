from django.db import models
from django.db.models import Sum
from api.v1.vendor.models import Vendor


class Product(models.Model):
    vendor      = models.ForeignKey(
                      Vendor,
                      on_delete=models.CASCADE,
                      related_name='products'
                  )
    name        = models.CharField('商品名稱', max_length=100)
    description = models.TextField('商品描述', blank=True)
    price       = models.DecimalField('售價', max_digits=10, decimal_places=2)
    stock       = models.PositiveIntegerField('庫存量', default=0)
    image       = models.ImageField('商品圖片', upload_to='products/', blank=True, null=True)
    sales_count = models.PositiveIntegerField('銷售數量', default=0)
    is_featured = models.BooleanField('精選商品', default=False)
    is_active   = models.BooleanField('啟用狀態', default=True)
    created_at  = models.DateTimeField('建立時間', auto_now_add=True)
    updated_at  = models.DateTimeField('更新時間', auto_now=True)

    class Meta:
        ordering = ['-sales_count', '-created_at']
        verbose_name = '商品'
        verbose_name_plural = '商品'

    def __str__(self):
        return self.name

    @property
    def total_sales(self):
        """計算總銷售量"""
        from api.v1.order.models import OrderItem
        return OrderItem.objects.filter(product=self).aggregate(
            total=Sum('quantity')
        )['total'] or 0

    def update_sales_count(self):
        """更新銷售數量"""
        self.sales_count = self.total_sales
        self.save(update_fields=['sales_count'])

    @property
    def is_in_stock(self):
        """檢查是否有庫存"""
        return self.stock > 0

    @property
    def stock_status(self):
        """庫存狀態"""
        if self.stock == 0:
            return 'out_of_stock'
        elif self.stock <= 5:
            return 'low_stock'
        else:
            return 'in_stock'