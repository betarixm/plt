import os
import binascii

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
            hash = str(binascii.hexlify(os.urandom(64)),'utf8')
            xss_trial = XssTrial.objects.create(hash=hash)
            xss_trial.from_team = request.user.username
            xss_trial.to_team = form.cleaned_data['team']
            xss_trial.csp = csp
            xss_trial.query = form.cleaned_data['query']
                                    
            if check_alert('http://'+get_current_site(request).domain+'/xss/'+hash):
                succeed = True
                flag = get_flag()

        return render(request, 'xss/xss.html', {
            'form': form,
            'succeed': succeed,
            'flag': flag,
        })


class XssTestView(View):
    def get(self, request, hash):
        data = XssTrial.objects.filter(hash = hash)
        print(data[0])
        if data[0]:
            return render(request, 'xss/xss_test.html', {
                'csp': data[0].csp,
                'query': data[0].query,
            })
        else:
            return render(request, 'xss/xss_test.html', {
                'csp': None,
                'query': None,
            })