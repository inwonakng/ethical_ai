from django.http import HttpResponse,JsonResponse, HttpRequest, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render, redirect
from .generation.Generator import Generator
from django.shortcuts import render
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

# Should view all of the surveys that this user has answered
def idx_view_answered_questions(request):
    context = {'ans':Survey.objects.filter(Q(user=request.user))}
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
    # return render(request, 'survey/base.html', {'form': form, 'registered': registered})

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
    HttpResponse(status=201)
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
            scen = rule.scenarios.all()[scenario_num].makecopy()

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
def save_scenario(request,scenario_id,rule_id,is_review):
    # if in review mode is_review == 1

    if not request.method == "POST": return
    # check if the survey exists for this combination already
    try:
        survey = Survey.objects.get(Q(user=request.user,ruleset_id=rule_id)) 
    except:
        survey = Survey(user=request.user,ruleset_id=rule_id)
        survey.save()

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
    #the list of rule sets by the parent_id
    #besides the features and its values in each scenario, their should also be values
    #including poll create date and number of participants
    
    context = {'rules':RuleSet.objects.filter(user_id = user_id).order_by('-creation_time'), 'user_id': user_id}
    return render(request, 'survey/my_survey.html', context)

@login_required
def survey_exporter(request,user_id,parent_id):
    # create a response with an attached csv file that gets written, inserting the survey information
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="survey_{id}.csv"'.format(id=parent_id)
    user_surveys = RuleSet.objects.filter(user_id=user_id)[parent_id-1]
    
    writer = csv.writer(response)
    writer.writerow(["ID", "Survey Title", "Prompt", "Number of responses", "Average time to complete survey", "Data created"])
    writer.writerow([str(user_surveys.id), str(user_surveys.rule_title), str(user_surveys.prompt), str(user_surveys.number_of_answers), str(7), str(user_surveys.creation_time)])

    return response

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


