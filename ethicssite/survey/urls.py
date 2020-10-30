from django.urls import path
from . import views

urlpatterns = [
    # this path is for mturk, where the random survey would be
    path('rules',views.rules_view,name='rules'),
    path('loadsurvey', views.load_survey, name='loadsurvey'),
    path('getscenario', views.get_scenario, name='getscenario'),
    path('rules_sample',views.rules_explain,name='rules_sample'),
    path('submit_result', views.submit_result, name="submitresult"),
    path('survey_result', views.survey_result, name="surveyresult"),
    path('<random>', views.unknown_path)
]
