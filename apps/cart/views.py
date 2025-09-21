from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse
from api.v1.product.models import Product
from .models import Cart, SessionCart
import json


def get_cart(request):
    """獲取用戶購物車"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    else:
        return SessionCart(request)


def cart_detail(request):
    """購物車詳情頁面"""
    cart = get_cart(request)
    
    if request.user.is_authenticated:
        cart_items = cart.items.select_related('product', 'product__vendor').all()
        context = {
            'cart': cart,
            'cart_items': cart_items,
            'total_price': cart.total_price,
            'total_items': cart.total_items,
        }
    else:
        cart_items = list(cart)
        total_price = cart.get_total_price()
        total_items = cart.get_total_items()
        context = {
            'cart_items': cart_items,
            'total_price': total_price,
            'total_items': total_items,
        }
    
    return render(request, 'cart/cart_detail.html', context)


@require_POST
def add_to_cart(request):
    """添加商品到購物車"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        # 檢查庫存
        if product.stock < quantity:
            return JsonResponse({
                'success': False,
                'message': f'庫存不足，目前僅有 {product.stock} 件'
            })
        
        cart = get_cart(request)
        
        if request.user.is_authenticated:
            cart.add_item(product, quantity)
            total_items = cart.total_items
        else:
            cart.add(product, quantity)
            total_items = cart.get_total_items()
        
        return JsonResponse({
            'success': True,
            'message': '商品已成功加入購物車',
            'total_items': total_items
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'加入購物車失敗: {str(e)}'
        })


@require_POST
def update_cart(request):
    """更新購物車商品數量"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id)
        cart = get_cart(request)
        
        if request.user.is_authenticated:
            cart.update_item_quantity(product, quantity)
            total_items = cart.total_items
            total_price = float(cart.total_price)
        else:
            if quantity <= 0:
                cart.remove(product)
            else:
                cart.add(product, quantity, override_quantity=True)
            total_items = cart.get_total_items()
            total_price = float(cart.get_total_price())
        
        return JsonResponse({
            'success': True,
            'message': '購物車已更新',
            'total_items': total_items,
            'total_price': total_price
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'更新失敗: {str(e)}'
        })


@require_POST
def remove_from_cart(request):
    """從購物車移除商品"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        
        product = get_object_or_404(Product, id=product_id)
        cart = get_cart(request)
        
        if request.user.is_authenticated:
            cart.remove_item(product)
            total_items = cart.total_items
            total_price = float(cart.total_price)
        else:
            cart.remove(product)
            total_items = cart.get_total_items()
            total_price = float(cart.get_total_price())
        
        return JsonResponse({
            'success': True,
            'message': '商品已從購物車移除',
            'total_items': total_items,
            'total_price': total_price
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'移除失敗: {str(e)}'
        })


@require_POST
def clear_cart(request):
    """清空購物車"""
    try:
        cart = get_cart(request)
        
        if hasattr(cart, 'clear'):
            cart.clear()
        else:
            # 如果是 SessionCart，確保有 clear 方法
            if hasattr(cart, 'cart'):
                cart.cart.clear()
                cart.save()
        
        return JsonResponse({
            'success': True,
            'message': '購物車已清空'
        })
        
    except Exception as e:
        print(f"清空購物車錯誤: {str(e)}")  # 用於調試
        return JsonResponse({
            'success': False,
            'message': f'清空失敗: {str(e)}'
        })


def cart_count(request):
    """獲取購物車商品數量（AJAX）"""
    cart = get_cart(request)
    
    if request.user.is_authenticated:
        count = cart.total_items
    else:
        count = cart.get_total_items()
    
    return JsonResponse({'count': count})


def merge_session_cart_to_user_cart(request):
    """將 session 購物車合併到用戶購物車（登入時調用）"""
    if not request.user.is_authenticated:
        return
    
    session_cart = SessionCart(request)
    if not session_cart.cart:
        return
    
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    
    for item in session_cart:
        product = item['product']
        quantity = item['quantity']
        user_cart.add_item(product, quantity)
    
    # 清空 session 購物車
    session_cart.clear()
