"""homework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.urls import path
from django.conf.urls import include, url
from django.conf.urls.static import static

from backend import search, views

urlpatterns = [
    path('api/', include('backend.urls')),
    path('admin/', admin.site.urls),
    path('search', search.search),
    url(r"^$", views.index),
    url('index', views.index, name="index"),
    url('detail', views.detail, name="detail"),
    url('login', views.to_login, name="login"),
    url('set', views.to_set, name="set"),
    url('star', views.to_star, name="star"),
    url('upload', views.to_upload, name="upload"),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
