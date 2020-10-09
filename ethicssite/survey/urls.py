from django.urls import path
from . import views

urlpatterns = [
    # this path is for mturk, where the random survey would be
    path('', views.random_survey, name='mturk'),
    path('getsurvey',views.get_survey,name='getsurvey'),
    path('result', views.survey_result, name="surveyresult"),
    path('<random>', views.unknown_path)
]