from django.urls import path
from django.conf.urls import url
from . import views
app_name = 'survey'
urlpatterns = [
    # this path is for mturk, where the random survey would be
    path('',views.idx_view_all_questions_trending,name='index'),
    path('trending',views.idx_view_all_questions_trending,name='trending'),
    path('latest',views.idx_view_all_questions_latest,name='latest'),
    path('ans',views.idx_view_answered_questions),
    path('res',views.idx_view_result_analysis),
    path('register', views.register, name='register'),
    url(r'^register/confirm/(?P<userid>\w+)/$', views.confirm_user, name='confirm_user'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('loadsurvey/<int:parent_id>', views.load_survey, name='loadsurvey'),
    path('getscenario/<int:parent_id>/<int:scenario_num>/<int:is_review>', views.get_scenario, name='getscenario'),
    path('savescenario/<int:scenario_id>/<int:rule_id>/<int:is_review>', views.save_scenario, name='savescenario'),
    path('review/<int:rule_id>',views.review_page,name='review'),
    path('submitsurvey',views.submit_survey,name='submitsurvey'),
    path('rules/lookup/',views.lookup_view),
    path('rules/lookup/<int:id>',views.dynamic_lookup_view),
    path('rules',views.rules_view,name='rules'),
    path('saverule',views.save_rule, name='saverule'),
    path('rulessample',views.rules_explain,name='rulessample'),
    path('surveyresult', views.survey_result, name="surveyresult"),
    path('mysurvey/<int:user_id>', views.my_survey, name='mysurvey'),
    path('<random>', views.unknown_path),

]
