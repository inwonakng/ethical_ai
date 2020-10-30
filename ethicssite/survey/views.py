from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseServerError
from .generation.Generator import Generator
from django.shortcuts import render
import yaml
from django.conf import settings
from .models import *


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


# stores everything into the Question model
def receive_survey(request):
    if request.method == "POST":
        questionString = request.POST['questionTitle']
        questionDesc = request.POST['desc']

        # set question string & description
        survey = Survey(question_txt=questionString,
                        question_desc=questionDesc)
        survey.save()

        # load the body as a json
        data = json.loads(request.body)

        # {0: info: {key: value, key: value, etc}, 1: info: {key: value, key: value, etc}}
        scenario_dict = {}

        # loop through json
        person_counter = 0
        for index in data:
            for key in index:
                value = index[key]
                if counter == 0:
                    scenario_dict[person_counter] = {"info": {key: value}}
                else:
                    scenario_dict[person_counter]["info"][key] = value
            person_counter += 1

        scenario = Scenario(number=person_counter,
                            prompt=scenario_dict, question=survey)
        scenario.save()

    pass

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
    survey_info = {}
    return render(request, 'survey/survey-page.html', survey_info)


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

# Django view to handle the survey results page.


def survey_result(request):
    results = [
        {'scenario': "1", 'features': ['feature1', 'feature2', 'feature3'], 'score': [
            ['A', 1], ['B', 2], ['C', 3]]},
        {'scenario': "2", 'features': ['feature1', 'feature2', 'feature3'], 'score': [
            ['A', 3], ['B', 4], ['C', 5]]},
        {'scenario': "3", 'features': ['feature1', 'feature2', 'feature3'], 'score': [
            ['A', 1], ['B', 7], ['C', 4]]}
    ]
    return render(request, 'survey/surveyresult.html', {'results': results})


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

    create_rule_set_from_json_string(json_rules_string)
    HttpResponse(statud=201)
