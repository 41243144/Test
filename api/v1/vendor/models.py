from django.db import models
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
import re

@register_snippet
class VendorCategory(models.Model):
    """商家分類"""
    name = models.CharField(max_length=255, verbose_name="分類名稱")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="網址名稱")
    description = models.TextField(blank=True, verbose_name="分類描述")
    color = models.CharField(
        max_length=7,
        default='#28a745',
        help_text="顏色代碼 (例如: #28a745)",
        verbose_name="分類顏色"
    )
    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Bootstrap Icons 圖示名稱 (例如: shop, truck)",
        verbose_name="圖示"
    )
    is_active = models.BooleanField(default=True, verbose_name="啟用狀態")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="排序")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    panels = [
        FieldPanel('name'),
        FieldPanel('slug', help_text="留空將自動根據名稱產生"),
        FieldPanel('description'),
        FieldPanel('color'),
        FieldPanel('icon'),
        FieldPanel('is_active'),
        FieldPanel('sort_order'),
    ]

    class Meta:
        verbose_name = "商家分類"
        verbose_name_plural = "商家分類"
        ordering = ['sort_order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug_from_chinese(self.name)
        super().save(*args, **kwargs)

    def generate_slug_from_chinese(self, text):
        """將中文文字轉換為適合的英文 slug"""
        chinese_to_english = {
            '農業商家': 'agriculture-vendor',
            '技術商家': 'technology-vendor',
            '食品商家': 'food-vendor',
            '市場商家': 'market-vendor',
            '教育商家': 'education-vendor',
        }

        if text in chinese_to_english:
            slug_base = chinese_to_english[text]
        else:
            slug_base = text.lower()
            for chinese, english in chinese_to_english.items():
                if chinese in text:
                    slug_base = slug_base.replace(chinese, english)

            if re.search(r'[\u4e00-\u9fff]', slug_base):
                slug_base = re.sub(r'[\u4e00-\u9fff]', '', slug_base)
                if not slug_base.strip():
                    slug_base = f"vendor-category-{self.pk or 'new'}"

            slug_base = re.sub(r'[^\w\s-]', '', slug_base)
            slug_base = re.sub(r'[\s_]+', '-', slug_base).strip('-')
            slug_base = slugify(slug_base) or f"vendor-category-{self.pk or 'new'}"

        original_slug = slug_base
        counter = 1
        while VendorCategory.objects.filter(slug=slug_base).exclude(pk=self.pk).exists():
            slug_base = f"{original_slug}-{counter}"
            counter += 1

        return slug_base

    def __str__(self):
        return self.name


class Vendor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vendor_profile'
    )
    name         = models.CharField('名稱', max_length=100)
    intro        = models.CharField('簡介', max_length=20, blank=True, null=True)
    description  = models.CharField('介紹', max_length=20, blank=True, null=True)
    address      = models.CharField('地址', max_length=255, blank=True, null=True)
    phone        = models.CharField('聯絡電話', max_length=20, blank=True, null=True)
    category     = models.ForeignKey(
        VendorCategory,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="分類"
    )
    created_at   = models.DateTimeField('建立時間', auto_now_add=True)
    updated_at   = models.DateTimeField('更新時間', auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.user.email})"