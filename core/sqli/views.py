from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django import forms
from .apps import query_sql
import json


class SqlQueryForm(forms.Form):
    query = forms.CharField()
    team = forms.CharField()


class SqliView(LoginRequiredMixin, View):
    def post(self, request):
        form = SqlQueryForm(json.loads(request.body.decode("utf-8")))
        if not form.is_valid():
            return JsonResponse({
                'success': False,
                'message': '공격을 시도할 지구를 선택해야합니다.'
            }, status=400)

        success, result, status_code = query_sql(request.user.username, form.cleaned_data['team'], form.cleaned_data['query'])
        return JsonResponse({
            'success': success,
            'message': str(result)
        }, status=status_code)
