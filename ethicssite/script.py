from random import randint
from django.db.models import Q
from survey.models import *
from survey.pref_pl.plackettluce import generate_pl_dataset as gen_pl
from joblib import load,dump
from survey.pref_pl.egmm_mixpl import egmm_mixpl as mixpl
from tqdm import tqdm
import numpy as np
from scipy.stats import rankdata
from collections import Counter

print('ok')

data = {
    'password1': 'XJLK2@dX',
    'password2': 'XJLK2@dX'
}

'''
# Code for nuking db
# ONLY USE THIS FOR CLEANING ENTIRE SURVEY

for s in Survey.objects.all():
    s.delete()

for s in RuleSet.objects.all():
    s.delete()

for s in Scenario.objects.all():
    s.delete()

for s in Option.objects.all():
    s.delete()

for u in User.objects.all():
    u.delete()
'''
# scores => permutation
# [1 3 5 5]  => [2 1 0 0]

# scores - 1,3,5,5
# permutation - [3,2,1,0] or [3,2,0,1] - this is what you should send

# clean the scores to work with egmm_mixpl
# example:
# def clean_sco(scores):

try:
    creator = User.objects.get(username = "user")
except:
    data['email'] = 'afakeema8il@gmail.com'
    data['username'] = 'user'
    form = UserForm(data)
    creator = form.save()
    creator.set_password('password')
    creator.is_active = True
    creator.save()

try:
    otheruser = User.objects.get(username="otheruser")
except:
    data['email'] = 'afakeema8il@gmail.com'
    data['username'] = 'otheruser'
    form = UserForm(data)
    otheruser = form.save()
    otheruser.set_password('')
    otheruser.is_active = True
    otheruser.save()

d = [
    {'question':'Who would you help first in an accident?',
    'options':[ 'A young boy', 
                'An old lady', 
                'A female teen',
                'A middle aged man']
    },
    {'question':'Who would you help first in an accident?',
    'options':[ 'A banker',
                'A student',
                'A doctor',
                'A mayor']
    },
    {'question':'Who would you help first in an accident?',
    'options':[ 'The mother', 
                'The father', 
                'The baby', 
                'The grandparents']
    }
]

try:
    seed = RuleSet.objects.get(rule_title='Demo survey for preference')
except:
    seed = json_to_ruleset(d,creator,
            'Demo survey for preference',
            'Mark the preferred options with higher values to rank the options')


seed.number_of_answers = 100
seed.save()

inputs = [ np.random.randint(10, size=(100, 4))
            for _ in range(3)]

for i in tqdm(range(100)):
    try:
        u = User.objects.get(username=f'user{i}')
    except:
        data['email'] = f'anemail{i}' + '@gmail.com'
        data['username'] = f'user{i}'
        form = UserForm(data)
        u = form.save()
        u.set_password('')
        u.is_active = True
        u.save()

    try:
        survey = Survey.objects.get(Q(user=u, ruleset_id=seed.id))
        for j,scen in enumerate(survey.scenarios.all()):
            for s,o in zip(inputs[j][i],scen.options.all()):
                o.score = s
                o.save()
            scen.save()
        survey.save()
    except:
        survey = Survey(user=u, ruleset_id=seed.id)
        survey.save()
        survey.prompt = seed.rule_title
        survey.save()
        survey.desc = seed.prompt
        survey.save()

        for j,s in enumerate(seed.scenarios.all()):
            scen = s.copy()
            for s,o in zip(inputs[j][i],scen.options.all()):
                o.score = s
                o.save()
            scen.save()
            survey.scenarios.add(scen)

dump(inputs,'pl_data')
print('success!')