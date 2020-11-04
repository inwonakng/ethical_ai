from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseServerError
from .generation.Generator import Generator
from django.shortcuts import render
import yaml
from django.conf import settings
from .models import *
from django import views
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def rules_view(request):
    if request.method == "POST":
        print("i'm in post request")
        print(request.POST);
        print(request.POST.getlist('rule_name'))
        print(request.POST.getlist('rule_set'))
        rule_names = request.POST.getlist('rule_name')
        rule_sets = request.POST.getlist('rule_set')

        # rs = RuleSet()
        # rs.save()
        #
        # ls = ListCateg(name="age")
        # ls.save()
        #
        # rsc = RuleSetChoice(index=1,value="asdf")
        # rsc.save()
        #
        # ls.choices.add(rsc)
        # rs.choice_categs.add(ls)
        test test
        rs = RuleSet()
        rs.save()
        for i,rule_name in enumerate(rule_names):
            print(rule_name)
            if rule_name:
                ls = ListCateg(name=rule_name)
                ls.save()
                print(rule_sets[i].split(','))
                rule_set = rule_sets[i].split(',')
                for j,val in enumerate(rule_set):
                    print(j,val)
                    rsc = RuleSetChoice(index=j,value=val)
                    rsc.save()
                    ls.choices.add(rsc)
                rs.choice_categs.add(ls)



        # rule_name = request.POST.get('rule_name')
        # rule_type = request.POST.get('rule_type')
        # RuleForm.objects.create(rule=rule_name,type=rule_type)

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
def load_survey(request):
    # empty for now
    survey_info = {}
    # survey_info.update(csrf(request))
    return render(request,'survey/survey-page.html',survey_info)

def get_scenario(request):
    combos = 3

    if request.method == "POST":
        combos = request.POST['combo_count']

    # grabbing the sample json
    rule = yaml.safe_load(
        open(settings.BASE_DIR+'/survey/generation/rule/rule.yaml', 'r'))
    # Survey
    if RuleSet.objects.all():
        # using defulat model here
        rr = RuleSet.objects.all()[0]
        story_gen = Generator(rule_model=rr)
    else:
        story_gen = Generator(rule=rule)
    ss = story_gen.get_scenario()
    survey_information = json.dumps(ss)
    # For frontend, check the html to
    # see how the object is grabbed.
    return HttpResponse(content=survey_information)

    # once you navigate to http://127.0.0.1:8000/survey/loadsurvey
    # and press ctrl+shift+i and switch to console tab,
    # you can see the json object printed on the console

# @csrf_exempt
def submit_survey(request):
    if request.method == 'POST':
        # for now not storing scores
        print('scenario:',request.body[0])
        print('scores:',request.body[1])

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


def rules_save(request):

    if request.method != 'POST':
        return HttpResponse(status=400)
    json_data = json.loads(request.body)
    json_rules_string = ''
    try:
        json_rules_string = json.dumps(json_data['rules'])
    except KeyError:
        HttpResponseServerError('`rules` field not found in request body.')

    json_to_ruleset(json_rules_string)
    HttpResponse(statud=201)
