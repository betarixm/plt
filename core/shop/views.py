from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from django.views import View
from utils.validator import unique_team_id
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
import json

from .models import Item
from env.environ import CATEGORY

Team = get_user_model()


class ShopView(LoginRequiredMixin, View):
    def get(self, request):
        item_list = {}
        for cate in CATEGORY:
            item_list[cate[1]] = [{"name": x.title,"id": x.id, "price": x.price, "already_bought": x.already_bought(request)} for x in Item.objects.filter(category=cate[0])]

        return JsonResponse({
            'money': request.user.balance,
            'item_list': item_list
        })


class ItemView(LoginRequiredMixin, View):
    def get(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return HttpResponse(status=404)
        
        return JsonResponse({
            'id': item_id,
            'name': str(item),
            'description': getattr(item, 'description'),
            'type': getattr(item, 'category'),
            'price': getattr(item, 'price'),
            'already_bought': item.already_bought(request)
        }, status=200)

    def post(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return HttpResponse(status=404)
        
        if item.already_bought(request):
            return HttpResponse(status=409)

        if not item.buy(request.user):
            return HttpResponse(status=402)
        return HttpResponse(status=200)