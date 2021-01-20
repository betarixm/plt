#from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django import forms
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
import json
from utils.validator import flag_format
from .apps import check_flag


class FlagAuthForm(forms.Form):
    flag = forms.CharField(validators=[flag_format])


class FlagAuthView(LoginRequiredMixin, View):
    def post(self, request):
        form = FlagAuthForm(json.loads(request.body.decode("utf-8")))
        user = request.user
        if not form.is_valid():
            return HttpResponse(status=400)
        
        is_ok, flag = check_flag(user, form.cleaned_data['flag'])
        if is_ok:
            return JsonResponse({
                'score': flag.score
            }, status=200)
        else:
            return HttpResponse(status=404)