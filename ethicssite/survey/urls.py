from django.urls import path
from . import views

urlpatterns = [
    # this path is for mturk, where the random survey would be
    path('rules',views.rules_view,name='rules'),
    path('loadsurvey', views.load_survey, name='loadsurvey'),
    path('getscenario', views.get_scenario, name='getscenario'),
    path('result', views.survey_result, name="surveyresult"),
    path('rules_sample',views.rules_explain,name='rules_sample'),
    path('<random>', views.unknown_path),
]
