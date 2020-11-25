from django.urls import path
from django.conf.urls import url
from . import views
app_name = 'survey'
urlpatterns = [
    # this path is for mturk, where the random survey would be
    path('',views.idx_view,name='index'),
    path('q1',views.desicion_questions_view),
    path('q2',views.delima_questions_view),
    path('register', views.register, name='register'),
    url(r'^register/confirm/(?P<userid>\w+)/$', views.confirm_user, name='confirm_user'),
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
