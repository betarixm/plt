from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django import forms
from django.views import View
from utils.validator import unique_team_id
from django.contrib.auth.mixins import LoginRequiredMixin
from .apps import create_team

Team = get_user_model()


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'core/index.html', {
            'name': request.user.username,
            'score': request.user.score,
            'money': request.user.balance,
        })


class RegisterForm(forms.Form):
    username = forms.CharField(validators=[unique_team_id])
    password = forms.CharField(min_length=8)
    email = forms.EmailField()


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'registration/register.html', {
            'form': form
        })

    def post(self, request):
        form = RegisterForm(request.POST)
        if not form.is_valid():
            return render(request, 'registration/register.html', {
                'form': form
            })

        team = create_team(
            form_username=form.cleaned_data['username'],
            form_password=form.cleaned_data['password'],
            form_email=form.cleaned_data['email'],
        )

        login(request, team)
        return redirect('/')


class DashboardView(View):
    def get(self, request):
        teams = Team.objects.all().exclude(is_superuser=True)
        teams = [(team.username, team.score) for team in teams]
        return render(request, 'core/dashboard.html', {
            'score_info': sorted(teams, key=lambda x: x[1], reverse=True)
        })
