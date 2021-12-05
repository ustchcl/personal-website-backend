from django.apps import AppConfig


class AuthenticationAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website.apps.authentication'
    label = 'authentication'
    verbose_name = 'Authentication'


default_app_config = 'website.apps.authentication.AuthenticationAppConfig'
