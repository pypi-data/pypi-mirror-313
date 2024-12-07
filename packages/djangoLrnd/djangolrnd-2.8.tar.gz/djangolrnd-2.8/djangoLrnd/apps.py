from django.apps import AppConfig
from django.conf import settings
from django.urls import include, path
from importlib import import_module

class DjangoLrndConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djangoLrnd'

    def ready(self):
        # Tambahkan middleware jika belum ada
        middleware = 'djangoLrnd.middleware.LRNDMiddleware'
        if middleware not in settings.MIDDLEWARE:
            settings.MIDDLEWARE += (middleware,)

        # Tambahkan aplikasi jika belum ada
        app_name = 'djangoLrnd'
        if app_name not in settings.INSTALLED_APPS:
            settings.INSTALLED_APPS += (app_name,)

        # Import modul urls.py proyek utama
        try:
            urlconf_module = import_module(settings.ROOT_URLCONF)
            
            # Pastikan urlpatterns sudah ada
            if not hasattr(urlconf_module, 'urlpatterns'):
                urlconf_module.urlpatterns = []
                
            # Tambahkan URL patterns djangoLrnd jika belum ada
            new_pattern = path('', include('djangoLrnd.urls'))
            if new_pattern not in urlconf_module.urlpatterns:
                urlconf_module.urlpatterns.append(new_pattern)
                
        except ImportError:
            # Handle jika modul tidak dapat diimpor
            pass
