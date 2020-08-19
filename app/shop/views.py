from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Item

from env.environ import ITEM_CATEGORY_SQLI, ITEM_CATEGORY_XSS, ITEM_CATEGORY_SSTI


class ShopView(LoginRequiredMixin, View):
    def get(self, request):
        items = Item.objects.all()
        return render(request, 'shop/shop.html', {
            'items': items
        })


class ItemView(LoginRequiredMixin, View):
    def get(self, request, item_id):
        item = Item.objects.filter(id=item_id)
        print(request.user.xss_filter.max_len)
        if len(item) == 0:
            return redirect('shop')

        item = item[0]
        already_buyed = False if len(Item.objects.filter(id=item_id, teams__username=request.user.username)) == 0 else True
        return render(request, 'shop/item_view.html', {
            'item': item,
            'already_buyed': already_buyed
        })

    def post(self, request, item_id):
        item = Item.objects.filter(id=item_id)

        if len(item) == 0:
            return redirect('shop')

        item = item[0]
        already_buyed = False if len(Item.objects.filter(id=item_id, teams__username=request.user.username)) == 0 else True

        if already_buyed:
            print("ALREADY")
            return redirect('shop')

        user = request.user

        if not item.buy(user):
            print("BALANCE")
            return redirect('shop')
        print(user.xss_filter.max_len)
        return redirect('shop')
