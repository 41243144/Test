from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin
from django.views.generic import RedirectView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

urlpatterns = [
    re_path(
        r'^admin/login/$',
        RedirectView.as_view(url='/accounts/login/', permanent=False),
        name='wagtail_admin_login_redirect'
    ),

    #re_path(r'^admin/users/.*$', users_not_found),
    path("admin/", include(wagtailadmin_urls)),
    path("search/", search_views.search, name="search"),

    ############## API URLS ##############
    path("api/v1/account/", include("api.v1.account.urls")),
    path("api/v1/order/", include("api.v1.order.urls")),
    path("api/v1/payment/", include("api.v1.payment.urls")),
    path("api/v1/vendor/", include("api.v1.vendor.urls")),

    ############## APP URLS ##############
    path('users/', include('apps.users.urls')),
    path('news/', include('apps.news.urls')),
    path('home/', include('apps.home.urls')),
    path('cart/', include('apps.cart.urls')),


    ############## THIRD-PARTY URLS ##############
    path('accounts/', include('allauth.urls')),
    path("documents/", include(wagtaildocs_urls)),
    #path("django-admin/", admin.site.urls),

]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
