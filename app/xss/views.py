from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from django import forms
from env.environ import team_choices

from .apps import attack_xss

# Create your views here.

class XssQueryForm(forms.Form):
    query = forms.CharField()
    team = forms.ChoiceField(choices=team_choices())


class XssView(LoginRequiredMixin, View):
    def get(self, request):
        form = XssQueryForm()
        return render(request, 'xss/xss.html', {
            'form': form
        })

    def post(self, request):
        form = XssQueryForm(request.POST)

        if not form.is_valid():
            return render(request, 'xss/xss.html', {
                'form': form
            })

        succeed = attack_xss(form.cleaned_data['team'], form.cleaned_data['query'])

        return render(request, 'xss/xss.html', {
            'form': form,
            'succeed': succeed
        })