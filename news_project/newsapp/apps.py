from django.apps import AppConfig


class NewsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsapp'

from django.apps import AppConfig

class NewsappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "newsapp"

    def ready(self):
        import newsapp.signals  # ✅ This ensures signals are loaded
