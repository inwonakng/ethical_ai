from django.http import HttpResponse, HttpRequest, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render, redirect
from .generation.Generator import Generator
from django.shortcuts import render
import yaml
import json
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


def idx_view_all_questions_trending(request):
    if request.user.id:
        context = {'rules':RuleSet.objects.filter(~Q(user=request.user)).order_by('-number_of_answers'),
                    'by':'trending'}
    else:
        context = {'rules':RuleSet.objects.all().order_by('-number_of_answers'), 'by':'trending'}
    print(context['by'])
    return render(request, "survey/all_questions.html", context)

def idx_view_all_questions_latest(request):
    print("asd")
    if request.user.id:
        context = {'rules':RuleSet.objects.filter(~Q(user=request.user)).order_by('-creation_time'),
                    'by':'latest'}
    else:
        context = {'rules':RuleSet.objects.all().order_by('-creation_time'), 'by':'latest'}
    print(context['by'])
    return render(request, "survey/all_questions.html", context)

def idx_view_answered_questions(request):
    context = {}
    return render(request, "survey/answered_questions.html", context)

def idx_view_result_analysis(request):
    context = {}
    return render(request, "survey/result_analysis.html", context)

def desicion_questions_view(request):
    context = {}
    return render(request, "survey/desicion_questions.html", context)

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
            mail.send_mail("Account Confirmation", "Please confirm your account registration.",
                            settings.EMAIL_HOST_USER, [user.email], html_message=html_msg)
        else:
            # fall through to rerendering register html with form.errors filled
            pass
            """
            for error in form.errors:
                print(error)
            """
    else:
        form = UserCreationForm()
    return render(request, 'survey/register.html', {'form': form, 'registered': registered})

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
                mail.send_mail("Account Confirmation", "Please confirm your account registration.",
                                settings.EMAIL_HOST_USER, [user.email], html_message=html_msg)
                return render(request, 'survey/login.html', {'error': 'Account was not activated. An activation link was resent to your email address.'})
        else:
            return render(request, 'survey/login.html', {'error': 'Invalid login details.'})
    else:
        return render(request, 'survey/login.html', {})

def user_logout(request):
    # the id is none if not logged in
    if not request.user.id:
        return redirect("/")
    logout(request)
    request.session.flush()
    return redirect('/')

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

'''
Page for users to create their own view
'''
def rules_view(request):
    context = {}
    return render(request, "survey/rules.html", context)

# Start survey

# Collect user input from survey

# page for user survey creation <-- ??
    # get user defined rules back <-- ??


# Function to grab new scenario
    # start survey
    # collect user input from survey
    # page for user survey creation
    # get user defined rules back
    # function to grab new scenario
def load_survey(request,parent_id):
    # empty for now
    rule = RuleSet.objects.get(id=parent_id)
    survey_info = {'parent_id':parent_id,'generative':rule.generative,'length':len(rule.scenarios.all())}

    if rule.generative:
        check = SurveyGenerator.objects.filter(rule_id = parent_id)
        if not check: build_generator(rule)

    # hardcoded!!!!!
    # grabbing default rule
    # rule = RuleSet.objects.all()[0]
    # check = SurveyGenerator.objects.filter(rule_id = rule.id)
    # if not check: build_generator(rule)

    # survey_info.update(csrf(request))
    return render(request,'survey/survey-page.html',survey_info)

def get_scenario(request,parent_id,scenario_num):

    rule = RuleSet.objects.get(id=parent_id)
    combos = 3

    if request.method == "POST":
        combos = request.POST['combo_count']


    '''
    Example of how a scenario object is created from the json.
    For @Taras, when you work on this, convert this function to return the model 
    rather than the json, so that the template can unpack the model instance there. 
    '''
    # if the survey is generative
    if rule.generative:
        # grabbing the sample json
        story_gen = SurveyGenerator.objects.get(rule_id=parent_id)
        # story_gen = SurveyGenerator.objects.get(rule_id=RuleSet.objects.all()[0].id)
        ss = story_gen.get_scenario()
        scen = Scenario()
        scen.save()
        for i,s in enumerate(ss):
            op = Option()
            op.name = 'Option '+ str(i)
            op.save()
            for k,v in s.items():
                attr = Attribute()
                attr.name = k
                attr.value = v
                attr.save()
                op.attributes.add(attr)
            op.save()
            scen.options.add(op)
    else:
        scen = rule.scenarios.all()[scenario_num]
        ss = [o.text for o in scen.options.all()]
    

    survey_information = json.dumps(ss)
    # For frontend, check the html to
    # see how the object is grabbed.
    return HttpResponse(content=survey_information)

    # once you navigate to http://127.0.0.1:8000/survey/loadsurvey
    # and press ctrl+shift+i and switch to console tab,
    # you can see the json object printed on the console

# Save individual scenario
def save_scenario(request):
    if request.method == "POST":
        # user id, session id, ruleset id
        user_id = request.post['user_id']
        session_id = request.post['session_id']
        ruleset_id = request.post['ruleset_id']
        # used to implement trending of index page.
        current_ruleset = RuleSet.objects.get(id=ruleset_id)
        current_ruleset.number_of_answers += 1
        current_ruleset.save()

        # prompt & description
        prompt = request.post['prompt']
        prompt_description = request.post['description']

        # not too sure how I'd take in a dictionary, but the idea is I somehow get a dictionary
        attribute_dictionary = request.post['dictionary']
        json_attribute = json.loads(attribute_dictionary)

        # slider score
        scenario_score = request.post['score']

        individual_scenario = Scenario()
        individual_scenario.save()
        individual_scenario.options.add(name=prompt, text=prompt_description)

        # saving each attribute (from dictionary)
        for key,value in json_attribute:
            individual_scenario.options.attributes.add(name=key, value=value)

        individual_scenario.options.score.add(value=scenario_score)

        # at this point, we have successfully created an individual_scenario object

        # now send that data to TempScenarios
        all_scenarios = TempScenarios(user_id=user_id, session_id=session_id, ruleset_id=ruleset_id)
        all_scenarios.save()
        all_scenarios.scenarios.add(individual_scenario)



# From gigantic list of scenarios create a Survey object
def create_survey(request):
    pass
    if request.method == "POST":
        user_id = request.post['user_id']
        session_id = request.post['session_id']
        ruleset_id = request.post['ruleset_id']
        # grab user id, session id, and ruleset id
        # filter
        # grab all objects of TempScenarios
        # create big survey
        # done!

        # filter for all the scenarios that relate to the ruleset id (along with other ids too)
        all_scenarios = TempScenarios.objects.filter(user_id=user_id).filter(session_id=session_id).filter(ruleset_id=ruleset_id)
        
        saved_survey = Scenario(prompt=prompt, desc=desc, user=user)
        saved_survey.save()

        # save scenario into survey
        for x in all_scenarios:
            saved_survey.scenarios.add(x)



# @csrf_exempt
@login_required
def submit_survey(request):
    return redirect('/')
    if request.method == 'POST':
        # for now not storing scores
        print(request.body)
        print('scenario:',request.body[0])
        print('scores:',request.body[1])
        print('asd', request.body[10])

        #Submits the json
        json_to_survey(request.body, request.user)
        # print(json.load(request.body))
        return redirect("survey:surveyresult")

def rules_explain(request):
    return render(request,'survey/rules_explain.html')

def survey_result(request):
    return render(request, 'survey/surveyresult.html')

# Django view to handle unknown paths
def unknown_path(request, random):
    return render(request, 'survey/unknownpath.html')

# Django endpoint to save rule to database from json post request body

@login_required
def save_rule(request):
    
    if request.method != 'POST':
        return HttpResponse(status=400)
    json_data = json.loads(request.body)
    # json_rules_string = ''
    
    # not doing error checks but we shoul dhave this later, i dont wanna do it now
    # try:
    #     json_rules_string = json.dumps(json_data['rules'])
    # except KeyError:
    #     HttpResponseServerError('`rules` field not found in request body.')

    
    json_to_ruleset(json_data['data'], request.user,json_data['title'],json_data['prompt'])
    HttpResponse(status=201)
    return redirect('/')

@login_required
def my_survey(request,user_id):
    #the list of rule sets by the parent_id
    #besides the features and its values in each scenario, their should also be values
    #including poll create date and number of particiants
    context = {'rules':RuleSet.objects.filter(user_id = user_id)}


    return render(request, 'survey/my_survey.html', context)
