from django.apps import AppConfig
from django.urls import include, path
from importlib import import_module

class DjangoLrndConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djangoLrnd'

    def ready(self):
        from django.conf import settings
        from .urls import djangoLrnd_url
        
        # Import modul urls.py proyek utama
        try:
            urlconf_module = import_module(settings.ROOT_URLCONF)
            
            # Pastikan urlpatterns sudah ada
            if not hasattr(urlconf_module, 'urlpatterns'):
                urlconf_module.urlpatterns = []
                
            # Tambahkan URL patterns djangoLrnd jika belum ada
            new_pattern = path('', include(djangoLrnd_url))
            if new_pattern not in urlconf_module.urlpatterns:
                urlconf_module.urlpatterns.append(new_pattern)
                
        except ImportError:
            # Handle jika modul tidak dapat diimpor
            pass
