from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django import forms
from .apps import get_sql_query
from env.environ import team_choices


class SqlQueryForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super(SqlQueryForm,self).__init__(*args,**kwargs)
        self.fields['team'].choices = team_choices()

    query = forms.CharField()
    team = forms.CharField()


class SqliView(LoginRequiredMixin, View):
    def get(self, request):
        form = SqlQueryForm()
        return render(request, 'sqli/sqli.html', {
            'form': form
        })

    def post(self, request):
        form = SqlQueryForm(request.POST)

        if not form.is_valid():
            return render(request, 'sqli/sqli.html', {
                'form': form
            })

        is_valid, result = get_sql_query(request.user.username, form.cleaned_data['team'], form.cleaned_data['query'])

        return render(request, 'sqli/sqli.html', {
            'form': form,
            'result': result,
            'is_valid': is_valid
        })
