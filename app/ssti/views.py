import requests

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from django import forms
from env.environ import team_choices
from .apps import check_ssti

# Create your views here.

class SstiQueryForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super(SstiQueryForm,self).__init__(*args,**kwargs)
        self.fields['team'].choices = team_choices()

    query = forms.CharField()
    team = forms.CharField()


class SstiView(LoginRequiredMixin, View):
    def get(self, request):
        form = SstiQueryForm()
        return render(request, 'ssti/ssti.html', {
            'form' : form
        })
    
    def post(self, request):
        form = SstiQueryForm(request.POST)

        if not form.is_valid():
            return render(request, 'ssti/ssti.html', {
                'form' : form
            })

        is_valid, result = check_ssti(form.team, form.query)
        return render(request, 'ssti/ssti.html', {
            'form' : form,
            'result': result,
            'is_valid': is_valid,
        })

        