from django.db import models


class HelpMessage(models.Model):
    user = models.ForeignKey('Users.User', on_delete=models.CASCADE, related_name='help_messages')
    subject = models.CharField(max_length=100)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def get_context(self):
        return {
            'id': self.id,
            'user': self.user.get_context(),
            'subject': self.subject,
            'message': self.message,
            'date_created': self.date_created.strftime('%Y-%m-%d %H:%M'),
        }

    def __str__(self):
        return f'{self.user.username} - {self.subject}'
