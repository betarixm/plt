from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from django import forms
from env.environ import team_choices
from django.contrib.sites.shortcuts import get_current_site

from .apps import prepare_xss, get_time_passed_after_last_attack, attack_xss
from env.xss.xss_flag import get_flag
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

        if not form.is_valid():
            return render(request, 'xss/xss.html', {
                'form': form,
                'failed': 'invalid form',
            })

        ok, csp = prepare_xss(form.cleaned_data['team'],
                                    form.cleaned_data['query'])
        if not ok:
            return render(request, 'xss/xss.html', {
                'form': form,
                'failed': 'blocked by length limit or regex filter',
            })

        time_passed_after_last_attack = get_time_passed_after_last_attack(request.user.username, form.cleaned_data['team'])
        if 5*60 - time_passed_after_last_attack > 0:
            return render(request, 'xss/xss.html', {
                'form': form,
                'failed': f"Next attack to Team [{form.cleaned_data['team']}] is available in {5*60 - time_passed_after_last_attack} seconds.",
            })

        xss_trial = attack_xss(request.user.username, 
                                form.cleaned_data['team'],
                                form.cleaned_data['query'],
                                csp)
        
        checked, succeed = check_alert(f'http://{get_current_site(request).domain}/xss/{xss_trial.hash}')
        xss_trial.checked = checked
        xss_trial.succeed = succeed
        xss_trial.save()

        if not checked:
            return render(request, 'xss/xss.html', {
                'form': form,
                'failed': "Python checkbot didn't worked. Please report to admin!!",
            })

        if not succeed:
            return render(request, 'xss/xss.html', {
                'form': form,
                'failed': "blocked by Content-Security-Policy! (or maybe your script is not alerting anything? you need to alert message.)",
            })

        flag = get_flag()

        return render(request, 'xss/xss.html', {
            'form': form,
            'failed': False,
            'flag': flag,
        })


class XssTestView(View):
    def get(self, request, hash):
        data = XssTrial.objects.filter(hash = hash)
        if data:
            return render(request, 'xss/xss_test.html', {
                'data': data[0],
            })
