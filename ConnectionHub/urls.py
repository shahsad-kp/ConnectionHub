"""ConnectionHub URL Configuration

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
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('djangoadmin/', admin.site.urls),
    path('', include('Home.urls')),
    path('', include('Auth.urls')),
    path('users/', include('Users.urls')),
    path('users/report/', include('Reports.urls')),
    path('post/comment/', include('Comments.urls')),
    path('post/', include('Posts.urls')),
    path('chat/', include('Communications.urls')),
    path('users/settings/', include('UsersSettings.urls')),
    path('admin/', include('Admin.AdminHome.urls')),
    path('admin/help/', include('Admin.AdminHelp.urls')),
    path('admin/post/', include('Admin.AdminPost.urls')),
    path('admin/reports/', include('Admin.AdminReports.urls')),
    path('admin/users/', include('Admin.AdminUsers.urls')),
    path('help/', include('Help.urls')),
    path('notifications/', include('Notifications.urls')),
]

urlpatterns = urlpatterns + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
urlpatterns = urlpatterns + static(
    settings.STATIC_URL,
    document_root=settings.STATICFILES_DIRS
)
