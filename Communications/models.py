from django.db import models

from ConnectionHub.settings import cipher_suite
from Users.models import User


class MessageUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(sender__is_banned=True).exclude(receiver__is_banned=True)


class Message(models.Model):
    sender = models.ForeignKey('Users.User', on_delete=models.CASCADE, related_name='sender_messages')
    receiver = models.ForeignKey('Users.User', on_delete=models.CASCADE, related_name='receiver_messages')
    timestamp = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)

    encrypted_message = models.BinaryField()

    @property
    def message(self):
        message_bytes = bytes(self.encrypted_message)
        return cipher_suite.decrypt(message_bytes).decode()

    @message.setter
    def message(self, value):
        self.encrypted_message = cipher_suite.encrypt(value.encode())

    objects = MessageUserManager()
    admin_objects = models.Manager()

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username}'

    @classmethod
    def not_blocked_messages(cls, logined_user: 'User'):
        return cls.objects.exclude(
            sender__blocked_users__user=logined_user
        ).exclude(
            receiver__blocked_users__user=logined_user
        )

    def get_context(self, logined_user: 'User'):
        return {
            'text': self.message,
            'sender': self.sender.get_context(logined_user),
            'receiver': self.receiver.get_context(logined_user),
            'timestamp': self.timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            'time': self.timestamp,
            'viewed': self.viewed,
            'is_sender': self.sender == logined_user,
        }
