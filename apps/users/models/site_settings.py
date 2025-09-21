from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import RichTextField
from wagtail.images import get_image_model_string
from wagtail.models import RevisionMixin, Site


@register_setting
class SiteBasicSetting(BaseGenericSetting, RevisionMixin):
    """
    網站基本設定
    讓管理員可以設定網站的基本資訊
    """
    
    # 網站基本資訊
    site_name = models.CharField(
        max_length=200,
        blank=True,
        default="尚虎雲平台",
        verbose_name="網站名稱",
        help_text="顯示在網站標題和頁面頂部的網站名稱"
    )
    
    site_tagline = models.CharField(
        max_length=255,
        blank=True,
        default="農業生產銷售一體化平台",
        verbose_name="網站標語",
        help_text="簡短描述網站的主要功能或特色"
    )
    
    site_description = RichTextField(
        blank=True,
        default="商互雲平台是一個專業的農業生產銷售一體化平台，致力於連接生產者與消費者，提供優質的農產品和服務。",
        verbose_name="網站描述",
        help_text="詳細描述網站的功能和服務，會顯示在關於我們頁面"
    )
    
    # Logo 和圖片
    site_logo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="網站 Logo",
        help_text="建議尺寸：200x60 像素，支援 PNG/JPG 格式"
    )
    
    favicon = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="網站圖示 (Favicon)",
        help_text="建議尺寸：32x32 像素，支援 PNG/ICO 格式"
    )
    
    # 聯絡資訊
    contact_email = models.EmailField(
        blank=True,
        default="contact@shanghuyun.com",
        verbose_name="聯絡信箱",
        help_text="主要聯絡信箱地址"
    )
    
    contact_phone = models.CharField(
        max_length=20,
        blank=True,
        default="+886-2-1234-5678",
        verbose_name="聯絡電話",
        help_text="主要聯絡電話號碼"
    )
    
    contact_address = models.TextField(
        blank=True,
        default="台北市信義區信義路五段7號",
        verbose_name="聯絡地址",
        help_text="公司或機構的實體地址"
    )
    
    # 社群媒體連結
    facebook_url = models.URLField(
        blank=True,
        verbose_name="Facebook 連結",
        help_text="Facebook 粉絲專頁網址"
    )
    
    twitter_url = models.URLField(
        blank=True,
        verbose_name="Twitter 連結",
        help_text="Twitter 帳號網址"
    )
    
    instagram_url = models.URLField(
        blank=True,
        verbose_name="Instagram 連結",
        help_text="Instagram 帳號網址"
    )
    
    youtube_url = models.URLField(
        blank=True,
        verbose_name="YouTube 連結",
        help_text="YouTube 頻道網址"
    )
    
    linkedin_url = models.URLField(
        blank=True,
        verbose_name="LinkedIn 連結",
        help_text="LinkedIn 公司頁面網址"
    )
    
    # SEO 設定
    default_meta_title = models.CharField(
        max_length=70,
        blank=True,
        default="尚虎雲平台 - 農業生產銷售一體化平台",
        verbose_name="預設 Meta 標題",
        help_text="搜尋引擎顯示的預設頁面標題，建議60-70字元"
    )
    
    default_meta_description = models.TextField(
        max_length=160,
        blank=True,
        default="尚虎雲平台提供完整的農業生產銷售解決方案，連接農民與消費者，打造可持續的農業生態系統。",
        verbose_name="預設 Meta 描述",
        help_text="搜尋引擎顯示的預設頁面描述，建議120-160字元"
    )
    
    google_analytics_id = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Google Analytics ID",
        help_text="Google Analytics 追蹤代碼，格式：GA_MEASUREMENT_ID"
    )
    
    google_tag_manager_id = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Google Tag Manager ID",
        help_text="Google Tag Manager 容器 ID，格式：GTM-XXXXXXX"
    )
    
    # 營業資訊
    business_hours = models.TextField(
        blank=True,
        default="週一至週五：09:00-18:00\n週六：09:00-17:00\n週日：休息",
        verbose_name="營業時間",
        help_text="營業時間說明"
    )
    
    support_email = models.EmailField(
        blank=True,
        default="support@shanghuyun.com",
        verbose_name="客服信箱",
        help_text="客戶服務專用信箱"
    )
    
    # （維護設定已移除）
    
    # 時間戳記
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")
    
    panels = [
        MultiFieldPanel([
            FieldPanel('site_name'),
            FieldPanel('site_tagline'),
            FieldPanel('site_description'),
        ], heading="網站基本資訊"),
        
        MultiFieldPanel([
            FieldPanel('site_logo'),
            FieldPanel('favicon'),
        ], heading="網站圖片"),
        
        MultiFieldPanel([
            FieldPanel('contact_email'),
            FieldPanel('contact_phone'),
            FieldPanel('contact_address'),
            FieldPanel('support_email'),
            FieldPanel('business_hours'),
        ], heading="聯絡資訊"),
        
        MultiFieldPanel([
            FieldPanel('facebook_url'),
            FieldPanel('twitter_url'),
            FieldPanel('instagram_url'),
            FieldPanel('youtube_url'),
            FieldPanel('linkedin_url'),
        ], heading="社群媒體連結"),
        
        MultiFieldPanel([
            FieldPanel('default_meta_title'),
            FieldPanel('default_meta_description'),
            FieldPanel('google_analytics_id'),
            FieldPanel('google_tag_manager_id'),
        ], heading="SEO 設定"),
        
    # 維護設定面板已移除
    ]
    
    class Meta:
        verbose_name = "網站基本設定"
        verbose_name_plural = "網站基本設定"
    
    def __str__(self):
        return f"網站基本設定 - {self.site_name}"
    
    @property
    def has_social_links(self):
        """檢查是否有設定任何社群媒體連結"""
        return any([
            self.facebook_url,
            self.twitter_url,
            self.instagram_url,
            self.youtube_url,
            self.linkedin_url,
        ])
    
    def get_social_links(self):
        """取得已設定的社群媒體連結"""
        links = []
        social_platforms = [
            ('facebook_url', 'Facebook', 'fab fa-facebook-f'),
            ('twitter_url', 'Twitter', 'fab fa-twitter'),
            ('instagram_url', 'Instagram', 'fab fa-instagram'),
            ('youtube_url', 'YouTube', 'fab fa-youtube'),
            ('linkedin_url', 'LinkedIn', 'fab fa-linkedin-in'),
        ]
        
        for field_name, platform_name, icon_class in social_platforms:
            url = getattr(self, field_name)
            if url:
                links.append({
                    'name': platform_name,
                    'url': url,
                    'icon': icon_class
                })
        
        return links

    # 兼容性方法：提供 for_request / for_site 以支援模板標籤與中間件的呼叫
    @classmethod
    def for_request(cls, request):
        """取得目前站點的設定；若為全域設定，回傳第一筆或 None。"""
        try:
            return cls.objects.first()
        except Exception:
            return None

    @classmethod
    def for_site(cls, site: Site):
        """與既有呼叫相容的替代方法，回傳全域設定第一筆或 None。"""
        try:
            return cls.objects.first()
        except Exception:
            return None
