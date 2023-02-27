"""ConnectionHub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Users
    2. Add a URL to urlpatterns:  path('', Users.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('MainHome.urls')),
    path('djangoadmin', admin.site.urls),
    path('users/', include('MainUsers.urls')),
    path('settings/', include('MainSettings.urls')),
    path('post/', include('MainPosts.urls')),
    path('admin/messages', include('AdminMessages.urls')),
    path('admin/reports/', include('AdminReports.urls')),
    path('admin/users/', include('AdminUsers.urls')),
    path('admin/post/', include('AdminPost.urls')),
    path('admin/', include('AdminHome.urls')),
]

urlpatterns = urlpatterns + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
