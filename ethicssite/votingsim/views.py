from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse, HttpRequest, HttpResponseServerError, HttpResponseRedirect
from django import views
from .models import *

# Create your views here.

def start(request):
    '''
    Renders the main page for voting rules
    '''

    return render(request,'votingsim/start.html',{})
    
def run_sim(request):
    '''
    Actually run the simulation using given arguments
    '''
    if request.method=='POST':
        form = VotingSimForm(request.POST)
    return redirect('votingsim:show_result')

def show_result(request):
    result,comment = compute_votingrules()

    return render(request,'votingsim/show_result.html',
                    {   'result':list(zip(*result.values())),
                        'comment':comment,
                    })


def compute_votingrules():
    result= {'v_rules':[ 'Copeland',
                        'Maximin',
                        'Borda',
                        'STV',
                        '0.6-ML',
                        '0.5-ML',],
            'conc_eff':['1.00',
                        '1.00',
                        '0.94',
                        '0.95',
                        '0.71',
                        '0.79',],
            'gr_fair':[ '0.79',
                        '0.78',
                        '0.79',
                        '0.80',
                        '0.95',
                        '0.94',],
            'savable':[ False,
                        False,
                        False,
                        False,
                        True,
                        True]}
    comment = "No traditional or newly designed voting rules empirically satisfy the requirements"
    return result,comment

def save_voting_rule(request):
    return