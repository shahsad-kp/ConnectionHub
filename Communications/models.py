from django.db import models

# from ConnectionHub.settings import cipher_suite
from Users.models import User


class Message(models.Model):
    message = models.CharField(max_length=255)
    sender = models.ForeignKey('Users.User', on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey('Users.User', on_delete=models.CASCADE, related_name='received_messages')
    timestamp = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username}'

    # def save(self, *args, **kwargs):
    #     self.content = cipher_suite.encrypt(self.message.encode()).decode()
    #     super(Message, self).save(*args, **kwargs)

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
