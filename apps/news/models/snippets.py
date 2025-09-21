from django.db import models
from django.utils.text import slugify
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
import re


@register_snippet
class NewsCategory(models.Model):
    """新聞分類"""
    name = models.CharField(max_length=255, verbose_name="分類名稱")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="網址名稱")
    description = models.TextField(blank=True, verbose_name="分類描述")
    color = models.CharField(
        max_length=7, 
        default='#007bff', 
        help_text="顏色代碼 (例如: #007bff)",
        verbose_name="分類顏色"
    )
    icon = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Bootstrap Icons 圖示名稱 (例如: newspaper, megaphone)",
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
        verbose_name = "最新消息區域-分類"
        verbose_name_plural = "最新消息區域-分類"
        ordering = ['sort_order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            # 將中文轉換為 slug
            self.slug = self.generate_slug_from_chinese(self.name)
        super().save(*args, **kwargs)

    def generate_slug_from_chinese(self, text):
        """將中文文字轉換為適合的英文 slug"""
        # 中文到英文的映射字典
        chinese_to_english = {
            '農業新聞': 'agriculture-news',
            '技術創新': 'technology-innovation',
            '市場行情': 'market-trends',
            '政策法規': 'policy-regulations',
            '有機農業': 'organic-farming',
            '智慧農業': 'smart-agriculture',
            '可持續發展': 'sustainable-development',
            '農產品認證': 'agricultural-certification',
            '食品安全': 'food-safety',
            '區塊鏈應用': 'blockchain-application',
            '最新消息': 'latest-news',
            '公告': 'announcement',
            '活動': 'events',
            '研究': 'research',
            '教育': 'education',
            '培訓': 'training',
            '合作': 'cooperation',
            '產業': 'industry',
            '環保': 'environmental',
            '科技': 'technology',
        }
        
        # 如果有直接映射，使用映射值
        if text in chinese_to_english:
            slug_base = chinese_to_english[text]
        else:
            # 嘗試部分匹配
            slug_base = text.lower()
            for chinese, english in chinese_to_english.items():
                if chinese in text:
                    slug_base = slug_base.replace(chinese, english)
            
            # 如果還包含中文字符，進行通用處理
            if re.search(r'[\u4e00-\u9fff]', slug_base):
                # 移除中文字符，只保留英文和數字
                slug_base = re.sub(r'[\u4e00-\u9fff]', '', slug_base)
                # 如果結果為空，使用默認名稱
                if not slug_base.strip():
                    slug_base = f"category-{self.pk or 'new'}"
            
            # 清理並格式化
            slug_base = re.sub(r'[^\w\s-]', '', slug_base)
            slug_base = re.sub(r'[\s_]+', '-', slug_base).strip('-')
            slug_base = slugify(slug_base) or f"category-{self.pk or 'new'}"
        
        # 確保 slug 的唯一性
        original_slug = slug_base
        counter = 1
        while NewsCategory.objects.filter(slug=slug_base).exclude(pk=self.pk).exists():
            slug_base = f"{original_slug}-{counter}"
            counter += 1
        
        return slug_base

    def __str__(self):
        return self.name


@register_snippet  
class NewsTag(models.Model):
    """新聞標籤"""
    name = models.CharField(max_length=100, unique=True, verbose_name="標籤名稱")
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="網址名稱")
    color = models.CharField(
        max_length=7, 
        default='#6c757d', 
        help_text="顏色代碼 (例如: #6c757d)",
        verbose_name="標籤顏色"
    )
    is_active = models.BooleanField(default=True, verbose_name="啟用狀態")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    panels = [
        FieldPanel('name'),
        FieldPanel('slug', help_text="留空將自動根據名稱產生"),
        FieldPanel('color'),
        FieldPanel('is_active'),
    ]

    class Meta:
        verbose_name = "最新消息-標籤"
        verbose_name_plural = "最新消息-標籤"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            # 將中文轉換為 slug
            self.slug = self.generate_slug_from_chinese(self.name)
        super().save(*args, **kwargs)

    def generate_slug_from_chinese(self, text):
        """將中文文字轉換為適合的英文 slug"""
        # 中文到英文的映射字典
        chinese_to_english = {
            '有機農業': 'organic-farming',
            '智慧農業': 'smart-agriculture', 
            '可持續發展': 'sustainable-development',
            '農產品認證': 'agricultural-certification',
            '食品安全': 'food-safety',
            '區塊鏈應用': 'blockchain-application',
            '人工智慧': 'artificial-intelligence',
            '機器學習': 'machine-learning',
            '物聯網': 'iot',
            '大數據': 'big-data',
            '雲端運算': 'cloud-computing',
            '精準農業': 'precision-agriculture',
            '溫室栽培': 'greenhouse-cultivation',
            '水耕栽培': 'hydroponic-cultivation',
            '生物技術': 'biotechnology',
            '基因改造': 'genetic-modification',
            '農藥殘留': 'pesticide-residue',
            '土壤改良': 'soil-improvement',
            '氣候變遷': 'climate-change',
            '碳足跡': 'carbon-footprint',
        }
        
        # 如果有直接映射，使用映射值
        if text in chinese_to_english:
            slug_base = chinese_to_english[text]
        else:
            # 嘗試部分匹配
            slug_base = text.lower()
            for chinese, english in chinese_to_english.items():
                if chinese in text:
                    slug_base = slug_base.replace(chinese, english)
            
            # 如果還包含中文字符，進行通用處理
            if re.search(r'[\u4e00-\u9fff]', slug_base):
                # 移除中文字符，只保留英文和數字
                slug_base = re.sub(r'[\u4e00-\u9fff]', '', slug_base)
                # 如果結果為空，使用默認名稱
                if not slug_base.strip():
                    slug_base = f"tag-{self.pk or 'new'}"
            
            # 清理並格式化
            slug_base = re.sub(r'[^\w\s-]', '', slug_base)
            slug_base = re.sub(r'[\s_]+', '-', slug_base).strip('-')
            slug_base = slugify(slug_base) or f"tag-{self.pk or 'new'}"
        
        # 確保 slug 的唯一性
        original_slug = slug_base
        counter = 1
        while NewsTag.objects.filter(slug=slug_base).exclude(pk=self.pk).exists():
            slug_base = f"{original_slug}-{counter}"
            counter += 1
        
        return slug_base

    def __str__(self):
        return self.name


@register_snippet
class NewsAuthor(models.Model):
    """新聞作者"""
    name = models.CharField(max_length=255, verbose_name="作者姓名")
    email = models.EmailField(blank=True, verbose_name="Email")
    bio = models.TextField(blank=True, verbose_name="個人簡介")
    avatar = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="頭像"
    )
    website = models.URLField(blank=True, verbose_name="個人網站")
    social_links = models.JSONField(
        default=dict,
        blank=True,
        help_text="社群媒體連結 JSON 格式",
        verbose_name="社群連結"
    )
    is_active = models.BooleanField(default=True, verbose_name="啟用狀態")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    panels = [
        FieldPanel('name'),
        FieldPanel('email'),
        FieldPanel('bio'),
        FieldPanel('avatar'),
        FieldPanel('website'),
        FieldPanel('social_links'),
        FieldPanel('is_active'),
    ]

    class Meta:
        verbose_name = "最新消息-發布者"
        verbose_name_plural = "最新消息-發布者"
        ordering = ['name']

    def __str__(self):
        return self.name
