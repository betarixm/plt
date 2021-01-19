from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django import forms
import json

from .apps import get_time_passed_after_last_attack, query_xss, create_flag
from env.environ import XSS_INTERVAL
from .models import XssLog

# Create your views here.

class XssQueryForm(forms.Form):
    query = forms.CharField()
    team = forms.CharField()


class XssView(LoginRequiredMixin, View):
    def post(self, request):
        form = XssQueryForm(json.loads(request.body.decode("utf-8")))
        
        if not form.is_valid():
            return JsonResponse({
                'success': False,
                'message': 'Invalid Form',
            }, status=400)

        time_passed_after_last_attack = get_time_passed_after_last_attack(request.user.username, form.cleaned_data['team'])
        if XSS_INTERVAL - time_passed_after_last_attack > 0:
            return JsonResponse({
                'success': False,
                'message': f"Please wait {XSS_INTERVAL - time_passed_after_last_attack} seconds",
            }, status=400)

        succeed, message, status_code = query_xss(request.user.username, form.cleaned_data['team'], form.cleaned_data['query'])
        if not succeed:
            return JsonResponse({
                'success': False,
                'message': message
            }, status=status_code)
        
        flag = create_flag()
        return JsonResponse({
            'success': True,
            'message': flag,
        }, status=status_code) # 200


class XssTestView(View):
    def get(self, request, hash):
        try:
            data = XssLog.objects.get(hash = hash)
            return render(request, 'xss/xss_test.html', {
                'data': data,
            })
        except XssLog.DoesNotExist:
            return HttpResponse(status=404)