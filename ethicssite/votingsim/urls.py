from django.urls import path,include
from django.conf.urls import url
from . import views
from rest_framework import routers

app_name = 'votingsim'

urlpatterns  = [
    path('start',views.start,name='start'),
    path('run_sim',views.run_sim,name='run_sim'),
    path('show_result',views.show_result,name='show_result'),
    path('save_voting_rule',views.save_voting_rule,name='save_voting_rule'),
]