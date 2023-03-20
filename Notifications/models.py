from django.db import models

from Users.models import User


class Notification(models.Model):
    notification_types = (
        ('like', 'like'),
        ('comment', 'comment'),
        ('follow', 'follow'),
        ('welcome', 'welcome'),
    )
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=notification_types)
    arg_value = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    viewed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.notification_type

    @classmethod
    def create_notification(cls, recipient: User, notification_type, content, arg_value=None):
        notification = cls(
            recipient=recipient,
            notification_type=notification_type,
            content=content,
        )
        if arg_value:
            notification.arg_value = arg_value
        notification.save()
        return notification

    def get_context(self):
        return {
            'id': self.id,
            'recipient': self.recipient.get_context(),
            'type': self.notification_type,
            'arg_value': self.arg_value,
            'content': self.content,
            'viewed': self.viewed,
            'timestamp': self.timestamp,
        }
