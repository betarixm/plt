from django.contrib import admin
from .models import Item, CspItem, LenItem, RegexItem

admin.site.register(CspItem)
admin.site.register(LenItem)
admin.site.register(RegexItem)