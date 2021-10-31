from django.urls import path,include
from django.conf.urls import url
from . import views
from rest_framework import routers

app_name = 'votingsim'

urlpatterns  = [
    path('run_sim',views.run_simulation,name='run_sim'),
    path('sample',views.get_sampleoutput,name='sample'),
    path('apply_rule',views.apply_rules,name='apply_rule'),
]