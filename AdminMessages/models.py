from django.db import models


class HelpMessage(models.Model):
    user = models.ForeignKey('MainUsers.User', on_delete=models.CASCADE, related_name='help_messages')
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return f'{self.user.username} - {self.subject}'
