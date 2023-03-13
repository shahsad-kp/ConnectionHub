from django.urls import path

from Notifications.views import notification_view, mark_as_viewed

urlpatterns = [
    path('', notification_view, name='notifications-view'),
    path('<int:notification_id>/mark-as-viewed/', mark_as_viewed, name='notification-viewed')
]
