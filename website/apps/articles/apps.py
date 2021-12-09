from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website.apps.articles'
    
    def ready(self):
        import website.apps.articles.signals
