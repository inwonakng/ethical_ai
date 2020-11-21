from django.contrib import admin

# Register your models here.
from .models import *

# admin.site.register(Survey)
admin.site.register(RuleSet)
# admin.site.register(Scenario)
# admin.site.register(Option)
admin.site.register(ListCateg)
admin.site.register(RuleSetChoice)
admin.site.register(Custom_rule)
