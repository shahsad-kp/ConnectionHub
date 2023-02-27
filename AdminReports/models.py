from django.db import models


class Report(models.Model):
    user = models.ForeignKey('MainUsers.User', on_delete=models.CASCADE, related_name="reports_users")
    reported_user = models.ForeignKey('MainUsers.User', on_delete=models.CASCADE, related_name="reports_reported")
    handled = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} reported {self.reported_user}'
