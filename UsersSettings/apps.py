from django.apps import AppConfig


class UserssettingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'UsersSettings'

    def ready(self):
        import UsersSettings.signals
