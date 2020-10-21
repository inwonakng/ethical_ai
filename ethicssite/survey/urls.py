from django.urls import path
from . import views

urlpatterns = [
    # this path is for mturk, where the random survey would be
    path('loadsurvey', views.load_survey, name='loadsurvey'),
    path('getscenario', views.get_scenario, name='getscenario'),
    path('survey/result', views.survey_result, name="surveyresult"),
    path('<random>', views.unknown_path)
]
