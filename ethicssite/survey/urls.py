from django.urls import path
from . import views

urlpatterns = [
    # this path is for mturk, where the random survey would be
    path('', views.random_survey, name='mturk'),
    path('submitsurvey', views.submit_survey, name='submitsurvey'),
    path('result', views.survey_result, name="surveyresult"),
    path('<random>', views.unknown_path)
]
