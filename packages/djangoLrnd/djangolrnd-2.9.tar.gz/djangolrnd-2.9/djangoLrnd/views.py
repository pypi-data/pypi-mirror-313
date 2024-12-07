import json

from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .middleware import LRNDMiddleware


@method_decorator(csrf_exempt, name='dispatch')
class ValidateView(View):
    template_name = 'djangoLrnd/validate.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            key = request.POST.get('key')
            
            if not key:
                messages.error(request, 'Kunci tidak ditemukan dalam data')
                return redirect('lrnd_validate')
            
            response = LRNDMiddleware.check_key_status(key)
            
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get('error') == 'Invalid Key':
                    messages.error(request, 'Kunci tidak valid')
                    return redirect('lrnd_validate')
                elif response_data.get('error') == 'Used':
                    messages.error(request, 'Kunci sudah digunakan')
                    return redirect('lrnd_validate')
                elif response_data.get('error') == 'Invalid Key Name':
                    messages.error(request, 'Nama kunci tidak valid')
                    return redirect('lrnd_validate')
                elif response_data.get('message') == 'Successfully':
                    LRNDKey = apps.get_model('djangoLrnd', 'LRNDKey')
                    LRNDKey.objects.update_or_create(id=1, defaults={'key': key})
                    success_redirect_url = getattr(settings, 'LRND_SUCCESS_REDIRECT_URL', '')
                    messages.success(request, 'Kunci berhasil divalidasi')
                    return redirect(success_redirect_url)
                else:
                    messages.error(request, 'Terjadi kesalahan saat memvalidasi kunci')
                    return redirect('lrnd_validate')
            else:
                messages.error(request, 'Terjadi kesalahan saat memvalidasi kunci')
                return redirect('lrnd_validate')
        
        except json.JSONDecodeError:
            messages.error(request, 'Data JSON tidak valid')
            return redirect('lrnd_validate')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('lrnd_validate')

validate_view = ValidateView.as_view()