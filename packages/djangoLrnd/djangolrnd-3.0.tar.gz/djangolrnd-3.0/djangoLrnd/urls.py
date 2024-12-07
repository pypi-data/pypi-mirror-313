from django.urls import path

from .views import validate_view

djangoLrnd_url = [
    path('validate/', validate_view, name='lrnd_validate'),
]