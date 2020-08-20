from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Item

from env.environ import ITEM_CATEGORY_SQLI, ITEM_CATEGORY_XSS, ITEM_CATEGORY_SSTI


class ShopView(LoginRequiredMixin, View):
    def get(self, request):
        category_list = [ITEM_CATEGORY_SQLI, ITEM_CATEGORY_SSTI, ITEM_CATEGORY_XSS]
        item_list = [(c.upper(), Item.objects.filter(category=c)) for c in category_list]
        return render(request, 'shop/shop.html', {
            'money': request.user.balance,
            'item_list': item_list
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
        result = lambda x: render(request, 'shop/result.html', {"msg": x})
        item = Item.objects.filter(id=item_id)

        if len(item) == 0:
            return redirect('shop')

        item = item[0]
        already_buyed = False if len(Item.objects.filter(id=item_id, teams__username=request.user.username)) == 0 else True

        if already_buyed:
            return result("이미 구매한 아이템이다구리!")

        user = request.user

        if not item.buy(user):
            return result("잔고가 모자라다구리...")

        print(user.xss_filter.max_len)
        return result("아이템 구매에 성공했다구리..!")
