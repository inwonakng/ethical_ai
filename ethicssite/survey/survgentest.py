from survey.models import *
import json
# rule_inp = json.load(open('survey/generation/rule/rule.json'))
# u = User.objects.all()[0]
# rule = json_to_ruleset(rule_inp,u,'titletitle','prompttasdfasdf')

rule = RuleSet.objects.get(id=34)
sg = build_generator(rule)