from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from autoslug import AutoSlugField

from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from .blocks import NewsContentStreamBlock
from .snippets import NewsCategory, NewsTag, NewsAuthor


class NewsIndexPage(Page):
    """新聞列表頁面"""
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="副標題")
    intro = RichTextField(blank=True, verbose_name="介紹文字")
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="橫幅圖片"
    )
    
    # SEO 設定
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        help_text="搜尋引擎描述 (建議 150-160 字元)",
        verbose_name="Meta 描述"
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text="搜尋關鍵字，用逗號分隔",
        verbose_name="Meta 關鍵字"
    )

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('intro'),
        FieldPanel('banner_image'),
    ]
    
    promote_panels = Page.promote_panels + [
        FieldPanel('meta_description'),
        FieldPanel('meta_keywords'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        
        # 取得所有已發布的新聞文章
        news_posts = NewsPost.objects.live().public().order_by('-first_published_at')
        
        # 分類篩選
        category_slug = request.GET.get('category')
        if category_slug:
            try:
                category = NewsCategory.objects.get(slug=category_slug, is_active=True)
                news_posts = news_posts.filter(category=category)
                context['current_category'] = category
            except NewsCategory.DoesNotExist:
                pass
        
        # 標籤篩選
        tag_slug = request.GET.get('tag')
        if tag_slug:
            try:
                tag = NewsTag.objects.get(slug=tag_slug, is_active=True)
                news_posts = news_posts.filter(tags=tag)
                context['current_tag'] = tag
            except NewsTag.DoesNotExist:
                pass
        
        # 搜尋功能
        search_query = request.GET.get('search')
        if search_query:
            news_posts = news_posts.search(search_query)
            context['search_query'] = search_query
        
        # 分頁
        paginator = Paginator(news_posts, 12)  # 每頁顯示 12 篇文章
        page_number = request.GET.get('page')
        
        try:
            news_posts = paginator.page(page_number)
        except PageNotAnInteger:
            news_posts = paginator.page(1)
        except EmptyPage:
            news_posts = paginator.page(paginator.num_pages)
        
        # 加入上下文
        context['news_posts'] = news_posts
        context['categories'] = NewsCategory.objects.filter(is_active=True)
        context['tags'] = NewsTag.objects.filter(is_active=True)
        
        return context

    class Meta:
        verbose_name = "新聞列表頁"
        verbose_name_plural = "新聞列表頁"


class NewsPost(Page):
    """新聞文章頁面"""
    
    # 基本資訊
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="副標題")
    excerpt = models.TextField(
        max_length=500,
        help_text="文章摘要，建議 150-300 字",
        verbose_name="文章摘要"
    )
    
    # 分類和標籤
    category = models.ForeignKey(
        NewsCategory,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="分類"
    )
    tags = models.ManyToManyField(
        NewsTag,
        blank=True,
        verbose_name="標籤"
    )
    
    # 作者資訊
    author = models.ForeignKey(
        NewsAuthor,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="作者"
    )
    
    # 圖片
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="特色圖片"
    )
    
    # 內容使用 StreamField
    content = StreamField(
        NewsContentStreamBlock(),
        verbose_name="文章內容",
        blank=True,
        use_json_field=True
    )
    
    # 發布設定
    is_featured = models.BooleanField(default=False, verbose_name="精選文章")
    is_top = models.BooleanField(default=False, verbose_name="置頂文章")
    allow_comments = models.BooleanField(default=True, verbose_name="允許留言")
    
    # SEO 設定
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        help_text="搜尋引擎描述 (建議 150-160 字元)",
        verbose_name="Meta 描述"
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text="搜尋關鍵字，用逗號分隔",
        verbose_name="Meta 關鍵字"
    )
    
    # 統計資訊
    view_count = models.PositiveIntegerField(default=0, verbose_name="瀏覽次數")
    like_count = models.PositiveIntegerField(default=0, verbose_name="按讚次數")
    
    # 相關設定
    related_posts = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        verbose_name="相關文章"
    )

    # 搜尋設定
    search_fields = Page.search_fields + [
        index.SearchField('subtitle'),
        index.SearchField('excerpt'),
        index.SearchField('content'),
        index.FilterField('category'),
        index.FilterField('tags'),
        index.FilterField('author'),
        index.FilterField('is_featured'),
        index.FilterField('is_top'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('excerpt'),
        MultiFieldPanel([
            FieldPanel('category'),
            FieldPanel('tags'),
            FieldPanel('author'),
        ], heading="分類與作者"),
        FieldPanel('featured_image'),
        FieldPanel('content'),
        MultiFieldPanel([
            FieldPanel('is_featured'),
            FieldPanel('is_top'),
            FieldPanel('allow_comments'),
        ], heading="發布設定"),
        FieldPanel('related_posts'),
    ]
    
    promote_panels = Page.promote_panels + [
        FieldPanel('meta_description'),
        FieldPanel('meta_keywords'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        
        # 增加瀏覽次數
        self.view_count += 1
        self.save(update_fields=['view_count'])
        
        # 取得相關文章
        related_posts = self.get_related_posts()
        context['related_posts'] = related_posts
        
        # 取得所有分類
        context['categories'] = NewsCategory.objects.filter(is_active=True)
        
        # 取得上一篇和下一篇文章
        context['previous_post'] = self.get_previous_post()
        context['next_post'] = self.get_next_post()
        
        return context
    
    def get_related_posts(self, limit=5):
        """取得相關文章"""
        # 優先顯示手動設定的相關文章
        manual_related = self.related_posts.live().public()
        if manual_related.exists():
            return manual_related[:limit]
        
        # 如果沒有手動設定，則根據分類和標籤自動推薦
        related = NewsPost.objects.live().public().exclude(id=self.id)
        
        if self.category:
            related = related.filter(category=self.category)
        
        if self.tags.exists():
            related = related.filter(tags__in=self.tags.all()).distinct()
        
        return related.order_by('-first_published_at')[:limit]
    
    def get_previous_post(self):
        """取得上一篇文章"""
        return NewsPost.objects.live().public().filter(
            first_published_at__lt=self.first_published_at
        ).order_by('-first_published_at').first()
    
    def get_next_post(self):
        """取得下一篇文章"""
        return NewsPost.objects.live().public().filter(
            first_published_at__gt=self.first_published_at
        ).order_by('first_published_at').first()

    def get_absolute_url(self):
        """取得文章的絕對 URL"""
        if self.category:
            return f"/news/{self.category.slug}/{self.slug}/"
        else:
            # 如果沒有分類，使用 ID
            return f"/news/{self.pk}/"

    def save(self, *args, **kwargs):
        # 自動設定 meta_description
        if not self.meta_description and self.excerpt:
            self.meta_description = self.excerpt[:160]
        
        # 使用 AutoSlugField 的方式自動生成 slug
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
            if not base_slug:
                # 如果標題是純中文無法轉換，使用簡單的識別碼
                import uuid
                base_slug = f"post-{uuid.uuid4().hex[:8]}"
            
            # 確保 slug 唯一性
            original_slug = base_slug[:50]
            slug = original_slug
            counter = 1
            while NewsPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                suffix = f"-{counter}"
                slug = f"{original_slug[:50-len(suffix)]}{suffix}"
                counter += 1
            self.slug = slug
        
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "新聞文章"
        verbose_name_plural = "新聞文章"


class NewsCategoryPage(Page):
    """新聞分類頁面"""
    
    category = models.ForeignKey(
        NewsCategory,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="分類"
    )
    description = RichTextField(blank=True, verbose_name="分類描述")
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="橫幅圖片"
    )

    content_panels = Page.content_panels + [
        FieldPanel('category'),
        FieldPanel('description'),
        FieldPanel('banner_image'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        
        # 取得該分類的所有文章
        news_posts = NewsPost.objects.live().public().filter(
            category=self.category
        ).order_by('-first_published_at')
        
        # 分頁
        paginator = Paginator(news_posts, 12)
        page_number = request.GET.get('page')
        
        try:
            news_posts = paginator.page(page_number)
        except PageNotAnInteger:
            news_posts = paginator.page(1)
        except EmptyPage:
            news_posts = paginator.page(paginator.num_pages)
        
        context['news_posts'] = news_posts
        context['category'] = self.category
        
        return context

    class Meta:
        verbose_name = "新聞分類頁"
        verbose_name_plural = "新聞分類頁"
