from django.http import HttpResponse,JsonResponse, HttpRequest, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render, redirect
from .generation.Generator import Generator
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from .models import *
from django import views
from django.core import mail
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django import forms

# for ML analysis
from .pref_pl.egmm_mixpl import egmm_mixpl as mixpl
from scipy.stats import rankdata
from collections import Counter
import numpy as np

# voting rules. Not ML but used with the ML stuff
from survey.pref_pl.voting_rules import Borda_winner,maximin_winner,plurality_winner
from .pref_pl.pl_voting import *

# for REST framework
from .serializers import *
from rest_framework import viewsets
from rest_framework import permissions
from wsgiref.util import FileWrapper
import yaml
import json
import csv
import os

# ====================
# View functions start
# ====================

'''
Returns a list of ID for all the 'RuleSet' the user has taken
'''
def check_taken(user):
    surveys = Survey.objects.filter(Q(user=user))
    return [s.ruleset_id for s in surveys]

def idx_view_all_questions_trending(request):
    if request.user.id: 
        queryset = RuleSet.objects.filter(~Q(user=request.user)).exclude(id__in=check_taken(request.user))
    else: queryset = RuleSet.objects.all()

    context = {'rules':queryset.order_by('-number_of_answers'), 'by':'trending'}
    print(context['by'])
    return render(request, "survey/all_questions.html", context)

def idx_view_all_questions_latest(request):
    if request.user.id: 
        queryset = RuleSet.objects.filter(~Q(user=request.user)).exclude(id__in=check_taken(request.user))
    else: queryset = RuleSet.objects.all()

    context = {'rules':queryset.order_by('-creation_time'), 'by':'latest'}
    print(context['by'])
    return render(request, "survey/all_questions.html", context)

def idx_view_answered_questions_earliest(request):
    queryset = Survey.objects.filter(Q(user=request.user))

    context = {'ans':queryset.order_by('date'), 'by': 'earliest'}
    return render(request, "survey/answered_questions.html", context)

def idx_view_answered_questions_latest(request):
    queryset = Survey.objects.filter(Q(user=request.user))
    context = {'ans':queryset.order_by('-date'), 'by': 'ans-latest'}
    return render(request, "survey/answered_questions.html", context)

def idx_view_result_analysis(request):
    context = {}
    return render(request, "survey/result_analysis.html", context)

def desicion_questions_view(request):
    context = {}
    return render(request, "survey/desicion_questions.html", context)


'''
Page for users to create their own view
'''
def rules_view(request):
    context = {}
    return render(request, "survey/rules.html", context)
# ====================
# View functions end
# ====================


# ====================
# User functions start
# ====================

def register(request):
    registered = False
    if request.method == "POST":
        form = UserForm(data=request.POST)

        if form.is_valid():
            user = form.save()

            # users are inactive until email verification
            user.is_active = False
            user.save()

            profile = UserProfile(user=user, creation_time=timezone.now())
            profile.save()

            # update registered variable for page to be rerendered
            registered = True

            html_msg = f"<p><a href='{request.build_absolute_uri('/register/confirm/')}{user.id}'>Click here to activate your account</a></p>"
            mail.send_mail("Account Confirmation", "Please confirm your account registration.", settings.EMAIL_HOST_USER, [user.email], html_message=html_msg)
            messages.info(request, "Success, you were sent an email with an account confirmation link!")
        else:
            # fall through to rerendering register html with form.errors filled
            pass
            """
            for error in form.errors:
                print(error)
            """
    else:
        form = UserCreationForm()
        messages.error("Invalid fields!")
    return HttpResponseRedirect('/')
    # return render(request, 'base.html', {'form': form, 'registered': registered})

def confirm_user(request, userid):
    user = get_object_or_404(User, pk=userid)

    # only activate and login if not already activated
    # (prevent link from being reused to allow others to login)
    if not user.is_active:
        user.is_active = True
        user.save()
        login(request, user)

    # TODO: add link expiration page / some error page

    # TODO: create a successful activation page?
    return redirect('/')

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            # TODO: check if user.is_active after setting up email confirmation
            if user.is_active:
                login(request, user)
                request.session['is_login'] = True
                request.session['user_name'] = username
                user_id = User.objects.filter(username = username).values('id').first()
                request.session['user_id'] = user_id['id']
                messages.success(request, "Logged in!")
                # redirect to previous page if sent from @login_required
                # else redirect to index
                if request.GET.get('next', False):
                    # TODO: fix, this redirecting doesn't seem to ever work
                    redirect(request.GET.get('next'))
                else:
                    return redirect('/')   
            else:
                # TODO: figure out how to actually determine if a user has confirmed email, inactive users don't show up in authenticate()
                # resend activation email
                html_msg = f"<p><a href='{request.build_absolute_uri('/register/confirm/')}{user.id}'>Click here to activate your account</a></p>"
                mail.send_mail("Account Confirmation", "Please confirm your account registration.", settings.EMAIL_HOST_USER, [user.email], html_message=html_msg)
                messages.error(request, "Account was not activated. An activation link was resent to your email address!")
                return HttpResponseRedirect('/')
        else:
            messages.error(request, "Invalid login details!")
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

def user_logout(request):
    # the id is none if not logged in
    if not request.user.id:
        return redirect("/")
    logout(request)
    request.session.flush()
    messages.success(request, "Logged out!")
    return HttpResponseRedirect('/')

# ====================
# User functions end
# ====================

# =============================
# Rule creation functions start
# =============================

def lookup_view(request):
    queryset = ListCateg.objects.all()
    context = {
        "obj_list":queryset
    }
    return render(request, "survey/lookup.html", context);

def dynamic_lookup_view(request,id):
    obj = ListCateg.objects.get(id=id)
    if request.method == "POST":
        obj.delete()
        return redirect("./")
    context = {
        "obj":obj
    }
    return render(request, "survey/delete.html", context)

# Django endpoint to save rule to database from json post request body
@login_required
def save_rule(request):
    
    if request.method != 'POST':
        return HttpResponse(status=400)
    json_data = json.loads(request.body)

    json_to_ruleset(json_data['data'], request.user,json_data['title'],json_data['prompt'])
    return redirect('/')

# =============================
# Rule creation functions end
# =============================


# =============================
# Survey taking section START
# =============================

def load_survey(request,parent_id):
    # prepare generator if generative survey
    rule = RuleSet.objects.get(id=parent_id)
    if rule.generative:
        check = SurveyGenerator.objects.filter(rule_id = parent_id)
        if not check: build_generator(rule)
    return redirect('survey:takesurvey', parent_id=parent_id, scenario_num=0, is_review=0)

def get_scenario(request,parent_id,scenario_num,is_review):
    # if in review mode is_review == 1

    rule = RuleSet.objects.get(id=parent_id)
    user = request.user
    # if the survey is generative
    if rule.generative:
        scen = SurveyGenerator.objects.get(rule_id=parent_id).get_scenario(user)
    else:
        # try getting it from an existing survey first
        try:
            surv = Survey.objects.get(Q(ruleset_id=parent_id,user=user))
            scen = surv.scenarios.all()[scenario_num]
        except:
            # this creates a new scenario object with same values..
            scen = rule.scenarios.all()[scenario_num].copy()

    context = {
        'rule':         rule,
        'curr_index':   scenario_num,
        'scenario':     scen,
        'is_review':    is_review
    }

    return render(request,'survey/takesurvey.html',context)

# review page for users to see their inputs
def review_page(request,rule_id):
    survey = Survey.objects.get(Q(user=request.user,ruleset_id=rule_id))
    # only covering case for custom surveys
    context = {'survey':survey}
    return render(request,'survey/review_survey.html',context)

def submit_survey(request):
    return redirect('/')

# Save individual scenario
def save_scenario(request,scenario_id,rule_id,is_review,survey_desc,survey_title):
    # if in review mode is_review == 1

    if not request.method == "POST": return
    # check if the survey exists for this combination already
    try:
        survey = Survey.objects.get(Q(user=request.user,ruleset_id=rule_id)) 
    except:
        survey = Survey(user=request.user,ruleset_id=rule_id)
        survey.save()
        survey.prompt = survey_title
        survey.save()
        survey.desc = survey_desc
        survey.save()
        seed = RuleSet.objects.get(id=rule_id)
        seed.number_of_answers += 1
        seed.save()

    # copy over the input valeus from request
    vals = list(request.POST.values())[1:]

    scenario = Scenario.objects.get(id=scenario_id)

    for o,sco in zip(scenario.options.all(),vals):
        o.score = sco
        o.save()
    scenario.save()
    survey.scenarios.add(scenario)
    survey.save()

    rule = RuleSet.objects.get(id = rule_id)

    num_scenarios = len(survey.scenarios.all())

    # if they are at the end of a survey
    if num_scenarios == rule.num_scenarios() or is_review==1:
        return redirect('survey:review',rule_id=rule_id)
    else: 
        return redirect('survey:takesurvey',parent_id=rule_id,scenario_num=num_scenarios,is_review=0)

# =============================
# Survey taking section END
# =============================


# =============================
# Extra endpoints start
# =============================

def rules_explain(request):
    return render(request,'survey/rules_explain.html')

def survey_result(request):
    return render(request, 'survey/surveyresult.html')

# Django view to handle unknown paths
def unknown_path(request, random):
    return render(request, 'survey/unknownpath.html')

# =============================
# Extra endpoints end
# =============================

# =============================
# User created survey start
# =============================

@login_required
def my_survey(request,user_id):
    if (user_id != request.user.id):
        messages.error(request, "You can't access survey data that you do not own!")
        return HttpResponseRedirect('/')
    if request.user.id != user_id:
        messages.error(request, "You can't access someone else's survey data!")
        return HttpResponseRedirect('/')
    else:
        #the list of rule sets by the parent_id
        #besides the features and its values in each scenario, their should also be values
        #including poll create date and number of participants
        user_specific_rules = []
        for x in RuleSet.objects.filter(user_id = user_id).order_by('-creation_time'):
            user_specific_rules.append(x)

        print(user_specific_rules)

        context = {'rules': user_specific_rules, 'user_id': user_id}
        return render(request, 'survey/my_survey.html', context)

@login_required
def survey_exporter(request,parent_id):
    # Check if user who's trying to download data owns that survey
    if (parent_id >= len(RuleSet.objects.all()) or parent_id <= 0):
        messages.error(request, "You can't download surveys that don't exist!")
        return HttpResponseRedirect('/')
    if (RuleSet.objects.all()[parent_id].user.id != request.user.id):
        messages.error(request, "You can't access someone else's survey data!")
        return HttpResponseRedirect('/')
    else:
        # create a response with an attached csv file that gets written, inserting the survey information
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="survey_{id}.csv"'.format(id=parent_id)
        user_surveys = RuleSet.objects.all()[parent_id]

        writer = csv.writer(response)
        writer.writerow(["ID", "Survey Title", "Prompt", "Number of responses", "Average time to complete survey", "Data created"])
        writer.writerow([str(user_surveys.id), str(user_surveys.rule_title), str(user_surveys.prompt), str(user_surveys.number_of_answers), str(7), str(user_surveys.creation_time)])

        return response

@login_required
def survey_info(request,parent_id):
    bag = RuleSet.objects.filter(id=parent_id)
    if not bag:
        messages.error(request, "You can't access surveys that don't exist!")
        return HttpResponseRedirect('/')
    if bag[0].user.id != request.user.id:
        messages.error(request, "You can't access someone else's survey data!")
        return HttpResponseRedirect('/')
    else:

        seed_rule = bag[0]
        score_per_scen = [[] for _ in seed_rule.scenarios.all()]

        for s in Survey.objects.filter(ruleset_id=seed_rule.id):
            if s.num_scenarios() == seed_rule.num_scenarios():
                for i,scen in enumerate(s.scenarios.all()):
                    score_per_scen[i].append(scen.get_scores())

        arr = score_per_scen
        # also store the scores as rankings. high values are preferred
        # returns ranks inside of each vote [9,2,5,0] => [1,3,2,4]
        ranks_per_scen = rankdata(10-np.array(score_per_scen),'ordinal',axis=2)

        # this is where the learned values are stored
        gammas_per_scen = [ (100*mixpl(s,len(s[0]),1)[0][1:]).tolist()
                            for s in score_per_scen
                            ]

        # parsing the rankings to get ranks for each option
        op_rank_per_scen = []
        for s in ranks_per_scen:
            per_scen = []
            for i,_ in enumerate(s[0]):
                votes = Counter(np.array(s)[:,i])
                ranks = [votes[j+1] for j,_ in enumerate(s[0])]
                per_scen.append(ranks)
            op_rank_per_scen.append(per_scen)


        # calculating voting rule winners
        voting_results = [{  
            'borda':(np.argsort(-Borda_winner(votes-1)[1])+1).tolist(),
            'plurality': (np.argsort(-plurality_winner(votes-1)[1])+1).tolist(),
            'maximin':(np.argsort(-maximin_winner(votes-1)[1])+1).tolist()}
                for votes in ranks_per_scen]
        
        pl_voting = [{
            'borda':(PL_Borda(np.array(g))[1]+1).tolist(),
            'plurality':(PL_plurality(np.array(g))[1]+1).tolist(),
            'maximin':(PL_maximin(np.array(g))[1]+1).tolist()}   
                for g in gammas_per_scen]

        context = {
            'rule': seed_rule, 
            'answer_dist': op_rank_per_scen, 
            'pl_gammas':gammas_per_scen,
            'survey_voting_results': voting_results,
            'pl_voting_results': pl_voting}
        return render(request, 'survey/survey_info.html', context)

# =============================
# User created survey end
# =============================

# =============================
# REST API functions start
# =============================

class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [permissions.AllowAny]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class ScenarioViewSet(viewsets.ModelViewSet):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
    # [q.object_form() for q in queryset]
    permission_classes = [permissions.AllowAny]

# this is for the mturk 
# function for creating an account for mturk users
def make_mturk_user(turk_id):
    query = Group.objects.filter(name='mturk')
    if query.exists(): group = query[0]
    else: 
        group = Group(name='mturk')
        group.save() 

    User.objects.filter(Q(username=turk_id)&Q(groups=group))

    user = User(password='',username=turk_id,is_active=True)
    user.save()
    user.groups.add(group)
    user.save()

    return user

@csrf_exempt 
def mturk_get_scenario(request):
    content = json.loads(request.body)

    uid = content['unique_id']
    survtype = content['survey_type']
    last_response = content['last_response']

    user_q = User.objects.filter(username=uid)
    if user_q.exists(): user = user_q[0]
    else: user = make_mturk_user(uid)

    if survtype == 'pair': 
        rulefile = os.path.join(settings.BASE_DIR,'survey/generation/rule/rule2.json')
        title = 'Mturk Pair'
        prompt = 'pair options for mturk'
    else:
        rulefile = os.path.join(settings.BASE_DIR,'survey/generation/rule/rule3.json')
        title = 'Mturk Triple'
        prompt = 'triple options for mturk'
        
    r_query = RuleSet.objects.filter(rule_title=title)
    if r_query.exists(): rule = r_query[0]
    else: rule = json_to_ruleset(  json.load(open(rulefile)),
                                        User.objects.get(username='admin'),
                                        title,
                                        prompt)

    survgen_q = SurveyGenerator.objects.filter(Q(rule = rule))    
    survey_q = Survey.objects.filter(Q(ruleset_id = rule.id) & Q(user = user))
    '''
    Need to record user response to past questions
    '''

    if survgen_q.exists(): survgen = survgen_q[0]
    else: survgen = build_generator(rule)

    if survey_q.exists(): survey = survey_q[0]
    else: 
        survey = Survey(prompt = 'mturk survey',
                        desc = 'for mturk',
                        ruleset_id = rule.id,
                        user = user)
        survey.save()
    
    scen = survgen.get_scenario(user)
    survey.scenarios.add(scen)
    survey.save()

    # fix formatting
    formatted = []
    for s in scen.object_form():
        dif_val = int(s.pop('survival difference').split('%')[0])
        wout_val = int(s['survival without jacket'].split('%')[0])
        # with_val = dif_val+wout_val
        s['survival with jacket'] = '{}%'.format(dif_val+wout_val)
        formatted.append(s)

    print('sending back...')
    print(formatted)

    return JsonResponse(formatted,safe=False)

def NLPSurvey(request):
    return render(request,'survey/NLPsurvey.html')

@csrf_exempt
# This is a hardcoded function for NLP classification task
def NLPSurvey_setup(request):
    username = request.body.decode()
    comments = OneComment.objects.filter(current__lt=3)

    # need to choose 2 datasets
    chosen = {
        'comments':[6],
        'datasets':[177],
        'entities':[2]
    }
    # for c in comments:
    #     if len(chosen == 20): break
    #     if not username in c.get_usernames():
    #         chosen.append({
    #             'dataset': c.dataset_index,
    #             'comment': c.comment_index,
    #         })
    #         c.add_user(username)

    return JsonResponse(chosen,safe=False)

# =============================
# REST API functions end
# =============================


