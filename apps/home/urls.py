from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('cooperative-farmers/', views.cooperative_farmers, name='cooperative_farmers'),
    path('vendor/<int:vendor_id>/products/', views.vendor_products, name='vendor_products'),
    path('vendor/<int:vendor_id>/product/<int:product_id>/', views.product_detail, name='product_detail'),
]
