from django.shortcuts import render
from django import forms
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.validator import flag_format
from .apps import check_flag


class FlagAuthForm(forms.Form):
    flag = forms.CharField(validators=[flag_format])


class FlagAuthView(LoginRequiredMixin, View):
    def get(self, request):
        form = FlagAuthForm()
        return render(request, 'flag/auth.html', {
            'form': form,
        })

    def post(self, request):
        form = FlagAuthForm(request.POST)
        user = request.user

        if not form.is_valid():
            return render(request, 'flag/auth.html', {
                'form': form
            })

        is_solved, flag = check_flag(user, form.cleaned_data['flag'])

        if is_solved:
            return render(request, 'flag/auth.html', {
                'form': form,
                'is_solved': is_solved,
                'd_score': flag.score
            })
        else:
            return render(request, 'flag/auth.html', {
                'form': form,
                'is_solved': is_solved
            })