from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from django.views import View
from utils.validator import unique_team_id
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
import json

from env.environ import CATEGORY

Team = get_user_model()


class ShopView(LoginRequiredMixin, View):
    def get(self, request):
        item_list = [(cate[1], Item.objects.filter(category=cate[0])) for cate in CATEGORY]
        return JsonResponse({
            'money': request.user.balance,
            'item_list': item_list
        })


class ItemView(LoginRequiredMixin, View):
    def get(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except model.DoesNotExist:
            return HttpResponse(status=404)
        
        try:
            item.get(teams__username=request.user.username)
            already_bought = True
        except model.DoesNotExist:
            already_bought = False
                  
        return JsonResponse({
            'id': item_id,
            'name': item,
            'description': getattr(item, 'description'),
            'type': getattr(item, 'category'),
            'price': getattr(item, 'price'),
            'already_bought': already_bought
        })

    def post(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except model.DoesNotExist:
            return HttpResponse(status=404)
        
        try:
            item.get(teams__username=request.user.username)
            return HttpResponse(status=409)
        except model.DoesNotExist:
            pass

        if not item.buy(request.user):
            return HttpResponse(status=402)
        return HttpResponse(status=200)