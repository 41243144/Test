from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count, Prefetch
from api.v1.vendor.models import Vendor, VendorCategory
from api.v1.product.models import Product

def cooperative_farmers(request):
    """合作小農頁面"""
    # 獲取所有商家，並預先載入相關的商品（前4個熱銷商品）
    top_products_prefetch = Prefetch(
        'products',
        queryset=Product.objects.filter(is_active=True).order_by('-sales_count', '-created_at')[:4],
        to_attr='top_products'
    )
    
    vendors = Vendor.objects.all().select_related('category', 'user').prefetch_related(
        top_products_prefetch
    )
    
    # 獲取分類
    categories = VendorCategory.objects.filter(is_active=True)
    
    # 統計資料
    stats = {
        'total_vendors': vendors.count(),
        'featured_vendors': 0,  # 當前模型沒有這個字段
        'verified_vendors': 0,  # 當前模型沒有這個字段
        'total_categories': categories.count(),
    }
    
    context = {
        'vendors': vendors,
        'categories': categories,
        'stats': stats,
    }
    
    return render(request, 'home/cooperative_farmers_new.html', context)

def vendor_products(request, vendor_id):
    """小農商品列表頁面"""
    vendor = get_object_or_404(Vendor, id=vendor_id)
    
    # 獲取該小農的所有商品
    products = Product.objects.filter(vendor=vendor, is_active=True).order_by('-sales_count', '-created_at')
    
    # 分頁處理（可選）
    from django.core.paginator import Paginator
    paginator = Paginator(products, 12)  # 每頁顯示12個商品
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'vendor': vendor,
        'products': page_obj,
        'total_products': products.count(),
    }
    
    return render(request, 'home/vendor_products.html', context)

def product_detail(request, vendor_id, product_id):
    """商品詳情頁面"""
    vendor = get_object_or_404(Vendor, id=vendor_id)
    product = get_object_or_404(Product, id=product_id, vendor=vendor, is_active=True)
    
    # 獲取相關商品（同一小農的其他商品）
    related_products = Product.objects.filter(
        vendor=vendor, is_active=True
    ).exclude(id=product_id).order_by('-sales_count')[:4]
    
    context = {
        'vendor': vendor,
        'product': product,
        'related_products': related_products,
    }
    
    return render(request, 'home/product_detail.html', context)
