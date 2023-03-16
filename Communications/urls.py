from django.urls import path

from . import views

urlpatterns = [
    path('', views.chat_list, name='chat-list'),
    path('<str:username>/', views.chat_list, name='chat-room'),
]
