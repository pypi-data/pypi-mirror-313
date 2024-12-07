import base64
import json
from datetime import datetime

import requests
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.urls import reverse


class LRNDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.validation_endpoint = getattr(settings, 'LRND_VALIDATION_ENDPOINT', 'http://127.0.0.1:8000/validate/')
        self.encryption_password = getattr(settings, 'LRND_ENCRYPTION_PASSWORD', 'password')
        self.exempt_paths = getattr(settings, 'LRND_EXEMPT_PATHS', ['/validate/'])
        self.key_model = getattr(settings, 'LRND_KEY_MODEL', 'djangoLrnd.LRNDKey')

    def __call__(self, request):
        if not self.is_path_exempt(request.path):
            if not self.is_valid(request):
                return redirect(reverse('lrnd_validate'))
        response = self.get_response(request)
        return response

    def is_path_exempt(self, path):
        return any(path.startswith(exempt_path) for exempt_path in self.exempt_paths)

    def is_valid(self, request):
        try:
            LRNDKey = apps.get_model('djangoLrnd', 'LRNDKey')
            key_instance = LRNDKey.objects.first()
        except Exception:
            raise ImproperlyConfigured("Tidak dapat mengambil instance LRNDKey")

        if not key_instance:
            return False

        try:
            decrypted_data = self.decrypt_data(key_instance.key, self.encryption_password)
            expiry_date = json.loads(decrypted_data)['expiry_date']
            expiry_date = datetime.fromisoformat(expiry_date)
            return expiry_date > datetime.now()
        except Exception:
            return False

    @staticmethod
    def check_key_status(key):
        password = getattr(settings, 'LRND_ENCRYPTION_PASSWORD', 'password')
        response = requests.post(settings.LRND_VALIDATION_ENDPOINT, json={'key': key, 'password': password}, headers={'Content-Type': 'application/json'})
        return response

    @staticmethod
    def create_key(password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    @classmethod
    def decrypt_data(cls, encrypted_data: str, password: str) -> str:
        decoded = base64.urlsafe_b64decode(encrypted_data)
        salt = decoded[:16]
        encrypted = decoded[16:]
        key = cls.create_key(password, salt)
        fernet = Fernet(key)
        return fernet.decrypt(encrypted).decode()