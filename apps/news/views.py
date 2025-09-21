from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.http import Http404
from .models import NewsPost, NewsCategory


class NewsListView(ListView):
    """最新消息列表頁面"""
    model = NewsPost
    template_name = 'news/news_list.html'
    context_object_name = 'news_posts'
    paginate_by = 6
    ordering = ['-first_published_at']
    
    def get_queryset(self):
        return NewsPost.objects.live().order_by('-first_published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = NewsCategory.objects.all()
        context['featured_posts'] = NewsPost.objects.live().filter(is_featured=True)[:3]
        return context


class NewsCategoryView(ListView):
    """分類消息列表頁面"""
    model = NewsPost
    template_name = 'news/news_category.html'
    context_object_name = 'news_posts'
    paginate_by = 6
    
    def get_queryset(self):
        self.category = get_object_or_404(NewsCategory, slug=self.kwargs['slug'])
        return NewsPost.objects.live().filter(category=self.category).order_by('-first_published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = NewsCategory.objects.all()
        return context


class NewsDetailView(DetailView):
    """消息詳細頁面"""
    model = NewsPost
    template_name = 'news/news_detail.html'
    context_object_name = 'news_post'
    
    def get_queryset(self):
        return NewsPost.objects.live()
    
    def get_object(self, queryset=None):
        """根據 URL 參數取得文章物件"""
        if queryset is None:
            queryset = self.get_queryset()
        
        # 如果是使用分類 + 文章 slug 的格式
        if 'category_slug' in self.kwargs and 'slug' in self.kwargs:
            category_slug = self.kwargs['category_slug']
            article_slug = self.kwargs['slug']
            
            # 取得分類
            category = get_object_or_404(NewsCategory, slug=category_slug)
            
            # 取得該分類下的文章
            return get_object_or_404(
                queryset,
                category=category,
                slug=article_slug
            )
        
        # 如果是使用 ID 的格式（備用）
        elif 'pk' in self.kwargs:
            return get_object_or_404(queryset, pk=self.kwargs['pk'])
        
        # 其他情況返回 404
        raise Http404("News post not found")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 獲取相關文章
        related_posts = NewsPost.objects.live().exclude(id=self.object.id)
        if self.object.category:
            related_posts = related_posts.filter(category=self.object.category)
        context['related_posts'] = related_posts[:3]
        context['categories'] = NewsCategory.objects.all()
        return context
