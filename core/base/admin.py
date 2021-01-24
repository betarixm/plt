from django.contrib import admin
from .models import Team, create_new_database, SqliFilter, XssFilter, RegexRule, CspRule, LenRule
        

admin.site.register(Team)
admin.site.add_action(create_new_database, "Create New Victim Database for SQL injection.")
admin.site.register(SqliFilter)
admin.site.register(XssFilter)
admin.site.register(RegexRule)
admin.site.register(CspRule)
admin.site.register(LenRule)
