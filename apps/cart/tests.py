from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from api.v1.vendor.models import Vendor, VendorCategory
from api.v1.product.models import Product
from apps.cart.models import Cart, CartItem
import json

User = get_user_model()


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.vendor_user = User.objects.create_user(
            email='vendor@example.com',
            password='testpass123'
        )
        self.category = VendorCategory.objects.create(
            name='測試分類',
            slug='test-category'
        )
        self.vendor = Vendor.objects.create(
            user=self.vendor_user,
            name='測試小農',
            category=self.category
        )
        self.product = Product.objects.create(
            vendor=self.vendor,
            name='測試商品',
            description='測試商品描述',
            price=100.00,
            stock=10
        )

    def test_cart_creation(self):
        """測試購物車創建"""
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(cart.user, self.user)
        self.assertTrue(cart.is_empty)
        self.assertEqual(cart.total_items, 0)
        self.assertEqual(cart.total_price, 0)

    def test_add_item_to_cart(self):
        """測試添加商品到購物車"""
        cart = Cart.objects.create(user=self.user)
        cart_item = cart.add_item(self.product, quantity=2)
        
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart.total_items, 2)
        self.assertEqual(cart.total_price, 200.00)

    def test_update_item_quantity(self):
        """測試更新商品數量"""
        cart = Cart.objects.create(user=self.user)
        cart.add_item(self.product, quantity=1)
        
        cart.update_item_quantity(self.product, 3)
        self.assertEqual(cart.total_items, 3)

    def test_remove_item_from_cart(self):
        """測試從購物車移除商品"""
        cart = Cart.objects.create(user=self.user)
        cart.add_item(self.product, quantity=2)
        
        cart.remove_item(self.product)
        self.assertTrue(cart.is_empty)


class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.vendor_user = User.objects.create_user(
            email='vendor@example.com',
            password='testpass123'
        )
        self.category = VendorCategory.objects.create(
            name='測試分類',
            slug='test-category'
        )
        self.vendor = Vendor.objects.create(
            user=self.vendor_user,
            name='測試小農',
            category=self.category
        )
        self.product = Product.objects.create(
            vendor=self.vendor,
            name='測試商品',
            description='測試商品描述',
            price=100.00,
            stock=10,
            is_active=True
        )

    def test_cart_detail_view(self):
        """測試購物車詳情頁面"""
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart_authenticated(self):
        """測試登入用戶加入購物車"""
        self.client.login(email='test@example.com', password='testpass123')
        
        response = self.client.post(
            reverse('cart:add_to_cart'),
            data=json.dumps({
                'product_id': self.product.id,
                'quantity': 2
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        
        # 檢查購物車是否有商品
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.total_items, 2)

    def test_add_to_cart_anonymous(self):
        """測試未登入用戶加入購物車"""
        response = self.client.post(
            reverse('cart:add_to_cart'),
            data=json.dumps({
                'product_id': self.product.id,
                'quantity': 1
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])

    def test_add_to_cart_insufficient_stock(self):
        """測試庫存不足時加入購物車"""
        response = self.client.post(
            reverse('cart:add_to_cart'),
            data=json.dumps({
                'product_id': self.product.id,
                'quantity': 20  # 超過庫存量
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['success'])
