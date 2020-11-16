from survey.models import *
from survey.generation import Generator as gen
gg = gen.Generator(rule_model = RuleSet.objects.all()[0])
sg = SurveyGenerator()
dd = Dict(json = gg.config)
dd.save()
sg.config = dd
sg.save()
for c in gg.combos:
    dd = Dict()
    dd.json = c.getCombo()
    dd.save() 
    sg.combos.add(dd)

rr = RuleSet.objects.all()[0]
rcategs = rr.range_categs.all()

from survey.models import *
sg = SurveyGenerator.objects.get(id=4)
sg.get_scenario()