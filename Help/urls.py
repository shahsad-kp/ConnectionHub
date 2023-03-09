from django.urls import path

from Help.views import help_view

urlpatterns = [
    path('', help_view, name='help-center'),
]