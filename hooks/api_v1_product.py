from wagtail_modeladmin.options import ModelAdmin, modeladmin_register 
from wagtail_modeladmin.views import CreateView, EditView, DeleteView
from wagtail.admin.panels import FieldPanel
from api.v1.product.models import Product
from api.v1.vendor.models import Vendor
from wagtail import hooks
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

class ProductCreateView(CreateView):
    def form_valid(self, form):
        if self.request.user.is_superuser:
            # cleaned_data 只有在 is_valid() 通過後才有
            vendor = form.cleaned_data.get('vendor')
        else:
            # 一般 vendor 自動綁定
            if not form.instance.pk:
                if not getattr(self.request.user, 'vendor_profile', None):
                    vendor = Vendor.objects.create(
                        user=self.request.user,
                        company_name=self.request.user.email
                    )
                    self.request.user.vendor_profile = vendor
                form.instance.vendor = self.request.user.vendor_profile
        return super().form_valid(form)


class ProductEditView(EditView):
    def dispatch(self, request, *args, **kwargs):
        """檢查編輯權限"""
        # 如果是超級管理員，允許編輯任何商品
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        
        # 從 URL 路徑中提取商品 ID
        import re
        path = request.path
        match = re.search(r'/edit/(\d+)/', path)
        
        if match:
            product_id = int(match.group(1))
            
            try:
                product = Product.objects.get(pk=product_id)
                
                # 檢查當前用戶是否擁有此商品
                user_vendor = None
                try:
                    user_vendor = request.user.vendor_profile
                except AttributeError:
                    try:
                        user_vendor = Vendor.objects.get(user=request.user)
                    except Vendor.DoesNotExist:
                        raise PermissionDenied("您沒有商家權限，無法編輯商品。")
                
                if user_vendor and product.vendor != user_vendor:
                    raise PermissionDenied(f"您只能編輯自己的商品。商品 '{product.name}' 不屬於您。")
                
            except Product.DoesNotExist:
                raise PermissionDenied("商品不存在。")
        
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(DeleteView):
    def dispatch(self, request, *args, **kwargs):
        """檢查刪除權限"""
        # 如果是超級管理員，允許刪除任何商品
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        
        # 從 URL 路徑中提取商品 ID
        import re
        path = request.path
        match = re.search(r'/delete/(\d+)/', path)
        
        if match:
            product_id = int(match.group(1))
            
            try:
                product = Product.objects.get(pk=product_id)
                
                # 檢查當前用戶是否擁有此商品
                user_vendor = None
                try:
                    user_vendor = request.user.vendor_profile
                except AttributeError:
                    try:
                        user_vendor = Vendor.objects.get(user=request.user)
                    except Vendor.DoesNotExist:
                        raise PermissionDenied("您沒有商家權限，無法刪除商品。")
                
                if user_vendor and product.vendor != user_vendor:
                    raise PermissionDenied(f"您只能刪除自己的商品。商品 '{product.name}' 不屬於您。")
                
            except Product.DoesNotExist:
                raise PermissionDenied("商品不存在。")
        
        return super().dispatch(request, *args, **kwargs)
    
class ProductAdmin(ModelAdmin):
    model = Product
    menu_label    = "商品管理"
    menu_icon     = "tag"
    list_display  = ("name", "vendor", "price", "stock")
    list_filter   = ("vendor",)
    search_fields = ("name", "vendor__company_name",)

    create_view_class = ProductCreateView
    edit_view_class = ProductEditView
    delete_view_class = ProductDeleteView

    panels = [
        FieldPanel('vendor', permission='superuser'),
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('price'),
        FieldPanel('stock'),
        FieldPanel('image'),
    ]

    def is_shown(self, request):
        return request.user.is_authenticated and (
            request.user.is_superuser or getattr(request.user, 'is_vendor', False)
        )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(vendor__user=request.user)

modeladmin_register(ProductAdmin)


@hooks.register("construct_image_chooser_queryset")
def _limit_image_chooser_to_own_uploads(images, request):
    """
    非超級管理員/非員工：圖片挑選器只顯示自己上傳的圖片
    超管/員工：不受限
    """
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return images
    if user.is_superuser or user.is_staff:
        return images
    return images.filter(uploaded_by_user=user)
