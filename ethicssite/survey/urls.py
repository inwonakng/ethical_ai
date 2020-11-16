from django.urls import path
from . import views
app_name = 'survey'
urlpatterns = [
    # this path is for mturk, where the random survey would be
    path('',views.IndexView.as_view(),name='index'),
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('rules',views.rules_view,name='rules'),
    path('loadsurvey/<int:parent_id>', views.load_survey, name='loadsurvey'),
    path('getscenario/<int:parent_id>', views.get_scenario, name='getscenario'),
    path('rulessample',views.rules_explain,name='rulessample'),
    path('submitsurvey', views.submit_survey, name="submitsurvey"),
    path('surveyresult', views.survey_result, name="surveyresult"),
    path('mypolls', views.my_polls, name='mypolls'),
    path('<random>', views.unknown_path),
    
]
