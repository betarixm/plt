from secrets import token_urlsafe

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.sites.shortcuts import get_current_site

from django import forms
from env.environ import team_choices

from .apps import prepare_xss
from .models import XssTrial
from .checkbot import check_alert

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
        flag = ""
        succeed = False

        if not form.is_valid():
            return render(request, 'xss/xss.html', {
                'form': form,
                'succeed': succeed,
            })
        
        res, csp = prepare_xss(form.cleaned_data['team'], form.cleaned_data['query'])
        if res:
            hash = token_urlsafe(30)
            xss_trial = XssTrial.objects.create(hash=hash)
            xss_trial.from_team = request.user.username
            xss_trial.to_team = form.cleaned_data['team']
            xss_trial.csp = csp
            xss_trial.query = form.cleaned_data['query']
                                    

            if check_alert('http://'+get_current_site(request).domain+'/xss/'+hash):
                succeed = True
                flag = getFlag(form.cleaned_data['team'])

        return render(request, 'xss/xss.html', {
            'form': form,
            'succeed': succeed,
            'flag': flag,
        })


class XssTestView(View):
    def get(self, request, hash):
        data = XssTrial.objects.filter(hash = hash)
        return render(request, 'xss/xss_test.html', {
            'csp': data.csp,
            'query': data.query,
        })