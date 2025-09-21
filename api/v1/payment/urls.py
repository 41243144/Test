from django.urls import path
from . import views

app_name = 'api.v1.payment'

urlpatterns = [
    path("checkout/<int:order_id>/", views.ecpay_checkout, name="ecpay_checkout"),
    path("notify/", views.ecpay_notify_url, name="notify_url"),
    path("order_result/", views.ecpay_order_result, name="order_result"),
]
