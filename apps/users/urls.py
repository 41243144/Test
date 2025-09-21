from django.urls import path
from django.views.generic import TemplateView


from .views import ProfilePageView, privacy_policy, terms_of_service


urlpatterns = [
    path('profile/', ProfilePageView.as_view(), name='profile'),
    path("privacy/", privacy_policy, name="privacy_policy"),
    path("terms-of-service/", terms_of_service, name="terms_of_service"),
]