from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from django.db import models

from ..blocks import HomePageStreamBlock


class HomePage(Page):
    """網站首頁頁面模型"""
    
    # StreamField 讓管理員可以自由編輯首頁內容
    body = StreamField(
        HomePageStreamBlock(),
        blank=True,
        verbose_name="首頁內容",
        help_text="使用區塊編輯器來建立首頁內容。可以新增、移動和刪除各種內容區塊。"
    )
    
    # 管理面板設定
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
    
    # 網頁模板
    template = 'home/home_page.html'
    
    class Meta:
        verbose_name = "首頁"
        verbose_name_plural = "首頁"


class CooperativeFarmersPage(Page):
    """合作小農頁面模型"""
    
    # StreamField 讓管理員可以自由編輯合作小農頁面內容
    body = StreamField(
        HomePageStreamBlock(),
        blank=True,
        verbose_name="頁面內容",
        help_text="使用區塊編輯器來建立合作小農頁面內容。可以新增、移動和刪除各種內容區塊。"
    )
    
    # 管理面板設定
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
    
    # 網頁模板
    template = 'home/cooperative_farmers_page.html'
    
    def get_context(self, request):
        """為模板提供合作小農相關的資料"""
        context = super().get_context(request)
        
        # 導入 vendor 模型
        from api.v1.vendor.models import Vendor, VendorCategory
        
        # 獲取所有商家
        vendors = Vendor.objects.all().select_related('category', 'user')
        
        # 獲取分類
        categories = VendorCategory.objects.filter(is_active=True)
        
        # 添加到 context
        context.update({
            'vendors': vendors,
            'categories': categories,
        })
        
        return context
    
    class Meta:
        verbose_name = "合作小農頁面"
        verbose_name_plural = "合作小農頁面"
