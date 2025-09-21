from django.db import models
from django.conf import settings
from api.v1.product.models import Product
from decimal import Decimal


class Cart(models.Model):
    """購物車模型"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='用戶'
    )
    created_at = models.DateTimeField('創建時間', auto_now_add=True)
    updated_at = models.DateTimeField('更新時間', auto_now=True)

    class Meta:
        verbose_name = '購物車'
        verbose_name_plural = '購物車'

    def __str__(self):
        return f"{self.user.email} 的購物車"

    @property
    def total_items(self):
        """購物車商品總數量"""
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        """購物車總價格"""
        return sum(item.total_price for item in self.items.all())

    @property
    def is_empty(self):
        """檢查購物車是否為空"""
        return not self.items.exists()

    def add_item(self, product, quantity=1):
        """添加商品到購物車"""
        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            product=product,
            defaults={'quantity': quantity, 'price': product.price}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return cart_item

    def remove_item(self, product):
        """從購物車移除商品"""
        try:
            item = self.items.get(product=product)
            item.delete()
            return True
        except CartItem.DoesNotExist:
            return False

    def update_item_quantity(self, product, quantity):
        """更新商品數量"""
        try:
            item = self.items.get(product=product)
            if quantity <= 0:
                item.delete()
            else:
                item.quantity = quantity
                item.save()
            return True
        except CartItem.DoesNotExist:
            return False

    def clear(self):
        """清空購物車"""
        self.items.all().delete()


class CartItem(models.Model):
    """購物車商品項目"""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='購物車'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='商品'
    )
    quantity = models.PositiveIntegerField('數量', default=1)
    price = models.DecimalField('單價', max_digits=10, decimal_places=2)
    created_at = models.DateTimeField('加入時間', auto_now_add=True)
    updated_at = models.DateTimeField('更新時間', auto_now=True)

    class Meta:
        verbose_name = '購物車商品'
        verbose_name_plural = '購物車商品'
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        """商品項目總價格"""
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        # 保存時更新價格為商品當前價格
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)


class SessionCart:
    """基於 Session 的購物車（未登入用戶）"""
    
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """添加商品到購物車"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """保存購物車到 session"""
        self.session.modified = True

    def remove(self, product):
        """從購物車移除商品"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """計算總價格"""
        return sum(Decimal(item['price']) * item['quantity'] 
                  for item in self.cart.values())

    def get_total_items(self):
        """計算總數量"""
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        """清空購物車"""
        if 'cart' in self.session:
            del self.session['cart']
        self.cart = {}
        self.save()

    def __iter__(self):
        """迭代購物車項目"""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """購物車項目數量"""
        return sum(item['quantity'] for item in self.cart.values())
