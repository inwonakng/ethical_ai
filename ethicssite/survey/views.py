from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .generation.Generator import Generator
from django.shortcuts import render
import yaml
from django.conf import settings
from .models import *

# stores everything into the Question model
def receive_survey(request):
    if request.method == "POST":
        questionString = request.POST['questionTitle']
        questionDesc = request.POST['desc']

        # set question string & description
        survey = Survey(question_txt=questionString, question_desc=questionDesc)
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

        scenario = Scenario(number=person_counter, prompt=scenario_dict, question=survey)
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
    return render(request,'survey/surveysample.html',survey_info)

def get_scenario(request):
    combos = 3

    if request.method == "POST":
        combos = request.POST['combo_count']


    # grabbing the sample json
    rule = yaml.safe_load(open(settings.BASE_DIR+'/survey/generation/rule/rule.yaml','r'))
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
                {'score': [0,3,7]},
                {'score': [7,7,7]},
                {'score': [6,6,6]}
              ]
    features = ['feature1', 'feature2','feature3']
    options = ['optionA', 'optionB', 'optionC']
    return render(request, 'survey/surveyresult.html', {'results':results, 'features':features, 'options': options})


# Django view to handle unknown paths
def unknown_path(request, random):
    return render(request, 'survey/unknownpath.html')
