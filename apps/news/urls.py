from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='list'),
    path('category/<slug:slug>/', views.NewsCategoryView.as_view(), name='category'),
    path('<slug:category_slug>/<slug:slug>/', views.NewsDetailView.as_view(), name='detail'),
    path('<int:pk>/', views.NewsDetailView.as_view(), name='detail_by_id'),  # 備用的ID訪問方式
]
