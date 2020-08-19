from django.contrib import admin
from .models import Team, SqliFilter, SstiFilter, XssFilter, RegexRule, CspRule, LenRule

# Register your models here.

admin.site.register(Team)
admin.site.register(SqliFilter)
admin.site.register(SstiFilter)
admin.site.register(XssFilter)
admin.site.register(RegexRule)
admin.site.register(CspRule)
admin.site.register(LenRule)