from django.apps import AppConfig
from django.urls import include, path

class DjangoLrndConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djangoLrnd'

    def ready(self):
        from django.conf import settings
        from .urls import djangoLrnd_url
        
        # Pastikan urlpatterns sudah ada
        if not hasattr(settings.ROOT_URLCONF, 'urlpatterns'):
            settings.ROOT_URLCONF.urlpatterns = []
            
        # Tambahkan URL patterns djangoLrnd
        settings.ROOT_URLCONF.urlpatterns.append(
            path('', include(djangoLrnd_url))
        ) 
