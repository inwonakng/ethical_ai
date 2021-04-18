from django.urls import path,include
from django.conf.urls import url
from . import views
from rest_framework import routers

app_name = 'votingsim'

urlpatterns  = [
    path('start',views.start,name='main')
]