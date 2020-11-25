from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseServerError, HttpResponseRedirect
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
    if not request.session.get('is_login',None):
        return redirect("/")
    logout(request)
    request.session.flush()
    return redirect('/')

def rules_view(request):
    # if request.method == "POST":
    #     print(request.POST.getlist('rule_name'))
    #     print(request.POST.getlist('rule_type'))
    #     rule_names = request.POST.getlist('rule_name')
    #     rule_types = request.POST.getlist('rule_type')
    #     for i,rule_name in enumerate(rule_names):
    #         RuleForm.objects.create(rule=rule_name,type=rule_types[i])
    #     # rule_name = request.POST.get('rule_name')
    #     # rule_type = request.POST.get('rule_type')
    #     # RuleForm.objects.create(rule=rule_name,type=rule_type)

    context = {}
    return render(request, "survey/rules.html", context)

class IndexView(views.generic.ListView):
    """
    Define homepage view, inheriting ListView class, which specifies a context variable.
    
    Note that login is required to view the items on the page.
    """
    
    template_name = 'survey/index.html'
    context_object_name = 'question_list'
    def get_queryset(self):
        """Override function in parent class and return all questions."""
        return Survey.objects.all().order_by('-pub_date')

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
    survey_info = {'parent_id':parent_id}

    check = SurveyGenerator.objects.filter(rule_id = parent_id)
    if not check: build_generator(RuleSet.objects.get(id=parent_id))
    
    # hardcoded!!!!!
    # grabbing default rule
    # rule = RuleSet.objects.all()[0]
    # check = SurveyGenerator.objects.filter(rule_id = rule.id)
    # if not check: build_generator(rule)

    # survey_info.update(csrf(request))
    return render(request,'survey/survey-page.html',survey_info)

def get_scenario(request,parent_id):
    combos = 3

    if request.method == "POST":
        combos = request.POST['combo_count']

    # grabbing the sample json
    story_gen = SurveyGenerator.objects.get(rule_id=parent_id)

    # story_gen = SurveyGenerator.objects.get(rule_id=RuleSet.objects.all()[0].id)

    ss = story_gen.get_scenario()
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
        

        # prompt & description
        prompt = request.post['prompt']
        prompt_description = request.post['description']

        # not too sure how I'd take in a dictionary, but the idea is I somehow DO get a dictionary (combo stuff)
        attribute_dictionary = request.post['dictionary']
        json_version = json.loads(attribute_dictionary)

        # slider score
        scenario_score = request.post['score']

        individual_scenario = Scenario()
        individual_scenario.save()
        individual_scenario.options.add(name=prompt, text=prompt_description)

        # saving each attribute (from dictionary)
        for key,value in json_version:
            individual_scenario.options.attributes.add(name=key, value=value)

        individual_scenario.options.score.add(value=scenario_score)

        # at this point, we have successfully created an individual_scenario object

        # now send that data to TempScenarios
        all_scenarios = TempScenarios(user_id=user_id, session_id=session_id, ruleset_id=ruleset_id)
        all_scenarios.save()
        all_scenarios.


        '''
            so in theory, we're taking in scenarios and saving them but we have to
            assign them a ruleset id so we can create a jumbo survey @ end
        '''

        # so now figure out how to take this scenario and shove it to a tempClass

# From gigantic list of scenarios create a Survey object
def create_survey(request):
    pass
    if request.method == "POST":
        user_id = request.post['user_id']
        session_id = request.post['session_id']
        ruleset_id = request.post['ruleset_id']
        # grab user id, session id, and ruleset id
        # grab all objects of TempScenarios
        # filter
        # create big survey
        # done!

        # filter for all the scenarios that relate to the ruleset id (along with other ids too)
        all_scenarios = TempScenarios.objects.filter(user_id=user_id).filter(session_id=session_id).filter(ruleset_id=ruleset_id)




# @csrf_exempt
@login_required
def submit_survey(request):
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
def rules_save(request):
    if request.method != 'POST':
        return HttpResponse(status=400)
    json_data = json.loads(request.body)
    json_rules_string = ''
    try:
        json_rules_string = json.dumps(json_data['rules'])
    except KeyError:
        HttpResponseServerError('`rules` field not found in request body.')

    json_to_ruleset(json_rules_string, request.user)
    HttpResponse(status=201)

@login_required
def my_polls(request,parent_id):
    #the list of rule sets by the parent_id
    #besides the features and its values in each scenario, their should also be values
    #including poll create date and number of particiants
    rulesets = RuleSet.objects.get(user_id = parent_id)

    return render(request, 'my_polls.html', {'asd':[1,2,3]})
