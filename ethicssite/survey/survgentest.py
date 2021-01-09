from survey.models import *
sg = SurveyGenerator.objects.all()[0]
uu = User.objects.all()[1]

scen = sg.get_scenario(uu)

