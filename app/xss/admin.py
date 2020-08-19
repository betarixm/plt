from django.contrib import admin

# Register your models here.

from .models import XssLog

admin.site.register(XssLog)