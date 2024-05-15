"""
URL configuration for recetas_lukas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from aparatos.sitemap import AparatosSitemap
from core.sitemap import RecetasSitemap
from django.contrib.sitemaps.views import sitemap


sitemaps = {
    'aparatos': AparatosSitemap,
    'recetas': RecetasSitemap,
}

# Ensure users go through the allauth workflow when logging into admin.
admin.site.login = staff_member_required(admin.site.login, login_url='/accounts/login')
# Run the standard admin set-up.
admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/two-factor/', include('allauth_2fa.urls')),
    path('accounts/', include('allauth.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
    path('aparatos/', include('aparatos.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('cookies/', include('cookie_consent.urls')),
    path('', include('core.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)