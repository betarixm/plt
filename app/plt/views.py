from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from env.environ import ITEM_CATEGORY_SQLI, ITEM_CATEGORY_XSS, ITEM_CATEGORY_SSTI


class HomeView(View):
    def get(self, request):
        return render(request, 'index.html', {})
