from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

# Create your views here.

class SstiView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'ssti.html', {})