from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse, HttpRequest, HttpResponseServerError, HttpResponseRedirect
from django import views
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import pickle
import codecs

import json 
from time import sleep
import pandas as pd
import xgboost as xgb
import numpy as np
from .sim_utility.xgboost_fair import gen_dataset, learn_voting_rule, just_test
from .sim_utility.fairness_new_tradeoffs import fairness_efficiency_all


# Create your views here.
@csrf_exempt
def run_simulation(request):
    print('ethicalapp: im here')
    # return JsonResponse('ok',safe=False)

    input = json.loads(request.body.decode())

    # This is what the example input would look like! (what the 'input' variable will contain)
    example_input = {   'no_candidates':    4,
                        'group_ratio':      0.33, 
                        'gr_fair_req':      0.80,
                        'conc_eff_req':     0.95,
                        'privacy_req':      'low',
                        'sim_runtime':      'mid',}
    
    input_keys = ['no_candidates,''group_ratio','gr_fair_req', 'privacy_req','sim_runtime',
                  'consistency', 'neutrality', 'monotonicity']
    
    # get group sizes and candidates
    m = input['no_candidates']
    z = input['group_ratio']
    if z < 0.5:
        z = 1-z
    n1 = int(20*z)
    n2 = 20 - n1
    
    # generate fair voting rules
    
    df = gen_dataset(n1, n2, m)
    xgboost_all, beta, uf, eff, sw = learn_voting_rule(df, n1, n2, m) 
    uf = 1-(n2)/(n1+n2) * uf
    srt_lvr = np.argsort(np.abs(uf-input['gr_fair_req']))
    lvr1 = xgboost_all[srt_lvr[0]]
    lvr2 = xgboost_all[srt_lvr[1]]
    
    base = f'{settings.BASE_DIR}/votingsim'

    lvr1_bin = codecs.encode(pickle.dumps(lvr1),'base64').decode()
    lvr2_bin = codecs.encode(pickle.dumps(lvr2),'base64').decode()


    # get info for other voting rules
    
    alpha, UF, UW, SWF, SWW, U, EFF = fairness_efficiency_all(n1, n2, m)
    voting_uf = np.mean(UF, axis = 0)
    voting_uf = round(1-(n2)/(n1+n2) * voting_uf ,3)
    voting_ef = round(np.mean(EFF, axis=0)[0] ,3)
    
    return JsonResponse({
            'tabledata':{
                # The display names go in columns
                'columns': ['Voting Rule','Condorcet Efficiency','Group Fairness', 
                            # 'Consistency', 'Monotonicity'
                            ],
                # The values go in rows
                'rows': [
                    ['Copeland',    '1.00',     voting_uf],
                    ['Maximin',     '1.00',     voting_uf],
                    ['Borda',       voting_ef,     voting_uf],
                    ['LVR1',        round(eff[srt_lvr[0]], 3),     round(uf[srt_lvr[0]], 3) ],
                    ['LVR2',        round(eff[srt_lvr[1]], 3),     round(uf[srt_lvr[1]], 3) ],
                ]
            },
            'remark': 'No traditional or newly designed voting rules empirically satisfy the requirements.',
            'learned_models':[
                {'name': 'LVR1',
                'type':'xgboost',
                'raw_data':lvr1_bin},
                {'name': 'LVR2',
                'type':'xgboost',
                'raw_data':lvr2_bin}
            ]
        },safe=False)

@csrf_exempt
def get_sampleoutput(request):
    input = json.loads(request.body.decode())

    # This is what the example input would look like! (what the 'input' variable will contain)
    example_input = {   'no_candidates':    4,
                        'group_ratio':      0.33, 
                        'conc_eff_req':     0.95,} # If the user has not filled out the fields, they are not included! (privacy/fairness/simulation)


    return JsonResponse({
            'tabledata':{
                'columns': ['Voting Rule','Condorcet Efficiency','Group Fairness'],
                'rows': [
                    ['Copeland',    '1.00',     '0.79'],
                    ['Maximin',     '1.00',     '0.78'],
                    ['Borda',       '0.94',     '0.79'],
                    ['STV',         '0.95',     '0.80'],
                    ['LVR1',        '0.71',     '0.95'],
                    ['LVR2',        '0.79',     '0.94'],
                ]
            },
            'remark': 'No traditional or newly designed voting rules empirically satisfy the requirements.\nThese values may not be exactly the same as the simulation output',
            'learned_models':[
                {'name': 'LVR1',
                'type':'xgboost',
                'raw_data':'Somethingsomething jsonified xgboost for LVR1'},
                {'name': 'LVR2',
                'type':'xgboost',
                'raw_data':'Somethingsomething jsonified xgboost for LVR2'}
            ]
        },safe=False)

@csrf_exempt
def apply_rules(request):
    input = json.loads(request.body.decode())
    # input contains 'preference profile' and 'learned voting rules'
    # Since we don't have a database, we can simply receive the json data back and rebuild the xgboost model (or any other model in future) in here
    
    example_input = {
        'preference_profile':{
            # allowed types are json,csv or plain text. They will all be parsed into a string when passed into backend
            'type':'csv',
            'raw_data':'string of veryveryvery long csv'
        },
        # This is the old input
        'sim_input': {  'no_candidates':    4,
                        'group_sizes':      0.33, 
                        'gr_fair_req':      0.80,
                        'conc_eff_req':     0.95,
                        'privacy_req':      'low',
                        'sim_data_size':    'mid'},

        'chosen_trad_rules': ['Borda'],
        'chosen_learned_rules':[{
            'name':'LVR1',
            'raw_data':'veryvery long jsonified xgboostmodel data'
        }]
    }

    rules = ['Copeland', 'Maximin', 'Borda', 'STV', 'LVR1', 'LVR2']
    # returns
    
    output_table = {
                'tabledata':{
                    # TESTCOL is just something I added to test 
                    'columns': ['Voting Rule','Condorcet Efficiency','Group Fairness','TESTCOL'],
                    'rows': [
                        ['Copeland',    '1.00',     '0.79',     '1'],
                        ['Maximin',     '1.00',     '0.78',     '1'],
                        ['Borda',       '0.94',     '0.79',     '1'],
                        ['STV',         '0.95',     '0.80',     '1'],
                        ['LVR1',        '0.71',     '0.95',     '1'],
                        ['LVR2',        '0.79',     '0.94',     '1'],
                    ]
                },
                'remark': 'Copeland: 1\nMaximin: 1\nBorda: 1\nSTV: 1\nLVR1: 2\nLVR2: 2',
                'learned_models':[
                    {'name': 'LVR1',
                    'type':'xgboost',
                    'raw_data':'Somethingsomething jsonified xgboost for LVR1'},
                    {'name': 'LVR2',
                    'type':'xgboost',
                    'raw_data':'Somethingsomething jsonified xgboost for LVR2'}
                ]
            }
    return JsonResponse(output_table,safe=False)