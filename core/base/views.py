#from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from django import forms
from django.views import View
from utils.validator import unique_team_id
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
import json

from env.environ import CATEGORY
from .apps import get_latest_attack

Team = get_user_model()


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return JsonResponse({
            'name': request.user.username,
            'score': request.user.score,
            'money': request.user.balance,
        })



class RegisterForm(forms.Form):
    username = forms.CharField(validators=[unique_team_id])
    password = forms.CharField(min_length=8)
    email = forms.EmailField()


class RegisterView(View):
    def post(self, request):
        form = RegisterForm(json.loads(request.body.decode("utf-8")))
        if not form.is_valid():
            return HttpResponse(status=400)

        Team.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
            email=form.cleaned_data['email'],
        )
        return HttpResponse(status=201)



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=8)


class LoginView(View):
    def post(self, request):
        form = LoginForm(json.loads(request.body.decode("utf-8")))
        if not form.is_valid():
            return HttpResponse(status=400)

        team = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )

        if team is not None:
            login(request, team)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=401)



class DashboardView(View):
    def get(self, request):
        ret = {}
        teams = Team.objects.all().exclude(is_superuser=True)
        for team in teams:
            ret[team.username] = {"score": team.score}
            for cate in CATEGORY:
                ret[team.username]["attacks"] = dict([(cate, get_latest_attack(team, cate)) for cate in CATEGORY])
            
        return JsonResponse(ret, status=200)
