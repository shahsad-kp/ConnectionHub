from django.db import models


class Report(models.Model):
    user = models.ForeignKey('Users.User', on_delete=models.CASCADE, related_name="reports_users")
    reported_user = models.ForeignKey('Users.User', on_delete=models.CASCADE, related_name="reports_reported")
    reason = models.CharField(max_length=255)
    handled = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} reported {self.reported_user}'

    def get_context(self):
        return {
            'id': self.id,
            'user': self.user.get_context(),
            'reported_user': self.reported_user.get_context(),
            'reason': self.reason,
            'date_created': self.date_created,
        }
