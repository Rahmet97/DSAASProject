from django.apps import AppConfig


class AuserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auser'

    def ready(self):
        import auser.signal
