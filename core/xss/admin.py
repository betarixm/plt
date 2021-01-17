from django.contrib import admin

from .models import XssLog

admin.site.register(XssLog)