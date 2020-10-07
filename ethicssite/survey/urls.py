from django.urls import path
from . import views

urlpatterns = [
    # this path is for mturk, where the random survey would be
    path('', views.randomsurvey, name='mturk'),
    path('getsurvey',views.getsurvey,name='getsurvey')
]