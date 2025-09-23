from django.shortcuts import render
import json
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Order, OrderItem
from api.v1.product.models import Product
import traceback

@csrf_exempt
def create_order(request):
    """
    Create an order with multiple products.
    Expected POST JSON format:
    {
        "items": [
            {"product_id": 1, "quantity": 2},
            {"product_id": 2, "quantity": 1}
        ]
    }
    """
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=400)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    try:
        data = json.loads(request.body)
        items_data = data.get("items", [])
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    if not items_data:
        return JsonResponse({"error": "No items provided"}, status=400)

    try:
        # Calculate total amount and validate products
        total_amount = 0
        products_to_add = []
        
        for item in items_data:
            try:
                product_id = int(item.get("product_id", 0))
                quantity = int(item.get("quantity", 1))
                
                if quantity <= 0:
                    return JsonResponse({"error": f"Invalid quantity for product {product_id}"}, status=400)
                
                product = get_object_or_404(Product, id=product_id, is_active=True)
                
                # Check stock availability
                if product.stock < quantity:
                    return JsonResponse({
                        "error": f"Insufficient stock for {product.name}. Available: {product.stock}, Requested: {quantity}"
                    }, status=400)
                
                total_amount += product.price * quantity
                products_to_add.append((product, quantity))
                
            except (ValueError, TypeError):
                return JsonResponse({"error": f"Invalid product data: {item}"}, status=400)

        # Create order (first save to generate ID for merchant_trade_no)
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
        )

        order.save()

        # Create order items and update stock
        order_items = []
        for product, qty in products_to_add:
            oi = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=qty,
                price=product.price
            )
            print(product.price)
            
            # Update product stock
            product.stock -= qty
            product.save()
            order_items.append({
                "product_id": oi.product.id,
                "name": oi.product.name,
                "quantity": oi.quantity,
                "price": float(oi.price),
                "total": float(oi.price * oi.quantity)
            })

        return JsonResponse({
            "success": True,
            "order_id": order.id,
            "merchant_trade_no": order.merchant_trade_no,
            "total_amount": float(order.total_amount),
            "status": order.status,
            "items": order_items,
            "message": "Order created successfully"
        })

    except Exception as e:
        # If order creation fails, rollback might be needed
        print(traceback.format_exc())
        return JsonResponse({"error": f"Order creation failed: {str(e)}"}, status=500)

def order_result(request):
    order_id = request.GET.get("order_id") 
    order = None

    if order_id:
        try:
            order = get_object_or_404(Order, id=int(order_id))
            # 確保只有訂單的所有者或管理員可以查看
            if request.user.is_authenticated and (order.user == request.user or request.user.is_staff):
                pass  # 允許查看
            else:
                order = None  # 不允許查看
        except (ValueError, TypeError):
            order = None

    context = {
        "order": order
    }
    return render(request, "order/order_result.html", context)


@login_required
def order_history(request):
    """用戶訂單紀錄"""
    # 獲取用戶的所有訂單，按創建時間倒序排列
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # 分頁處理
    paginator = Paginator(orders, 10)  # 每頁顯示10個訂單
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 狀態篩選
    status_filter = request.GET.get('status')
    if status_filter and status_filter != 'all':
        orders = orders.filter(status=status_filter)
        paginator = Paginator(orders, 10)
        page_obj = paginator.get_page(page_number)
    
    # 統計數據
    total_orders = orders.count()
    pending_orders = Order.objects.filter(user=request.user, status='pending').count()
    completed_orders = Order.objects.filter(user=request.user, status='completed').count()
    
    context = {
        'page_obj': page_obj,
        'orders': page_obj.object_list,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'current_status': status_filter or 'all',
    }
    
    return render(request, "order/order_history.html", context)
