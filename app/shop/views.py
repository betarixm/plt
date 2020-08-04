from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Item

from env.environ import ITEM_CATEGORY_SQLI, ITEM_CATEGORY_XSS, ITEM_CATEGORY_SSTI


class ShopView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'shop.html', {})


class ItemListView(LoginRequiredMixin, View):
    def get(self, request):
        sqli_items = Item.objects.filter(category=ITEM_CATEGORY_SQLI)
        ssti_items = Item.objects.filter(category=ITEM_CATEGORY_SSTI)
        xss_items = Item.objects.filter(category=ITEM_CATEGORY_XSS)

        return render(request, 'shopItemList.html',{
            'sqli': sqli_items,
            'xss': xss_items,
            'ssti': ssti_items
        })

