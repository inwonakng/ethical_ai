from django.urls import path
from django.conf.urls import url
from . import views
app_name = 'survey'
urlpatterns = [
    # this path is for mturk, where the random survey would be
    path('',views.IndexView.as_view(),name='index'),
    path('register', views.register, name='register'),
    url(r'^register/confirm/(?P<userid>\w+)/$', views.confirm_user, name='confirm_user'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('rules',views.rules_view,name='rules'),
    path('loadsurvey', views.load_survey, name='loadsurvey'),
    path('getscenario', views.get_scenario, name='getscenario'),
    path('rulessample',views.rules_explain,name='rulessample'),
    path('submitsurvey', views.submit_survey, name="submitsurvey"),
    path('surveyresult', views.survey_result, name="surveyresult"),
    path('<random>', views.unknown_path)
]
