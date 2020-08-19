from django.contrib import admin

# Register your models here.

from .models import SqliLog

admin.site.register(SqliLog)