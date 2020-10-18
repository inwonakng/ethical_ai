from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .generation.Generator import Generator
from django.shortcuts import render
import json

# stores everything into the Question model


def receive_survey(request):
    if request.method == "POST":
        questionString = request.POST['questionTitle']
        questionDesc = request.POST['desc']

        # set question string & description
        survey = Survey(question_txt=questionString, question_desc=questionDesc)
        survey.save()

        data = request.post['scenario_data']

        # set scenarios
        scenario = Scenario(prompt=data, question=survey)
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
    return render(request,'',{})

def get_scenario(request):
    # grabbing the sample json
    rule = json.load(open('ethicssite/survey/generation/rule/rule.json','r'))
    story_gen = Generator(rule=rule)
    ss = story_gen.get_scenario()
    survey_information = json.dumps(ss)
    # For frontend, check the html to
    # see how the object is grabbed.
    return render(request,
                  'survey/surveysample.html', context={"survey_information": survey_information})

    # once you navigate to http://127.0.0.1:8000/survey/loadsurvey
    # and press ctrl+shift+i and switch to console tab,
    # you can see the json object printed on the console

# Django view to handle the survey results page.
def survey_result(request):
    results = {}
    return render(request, 'survey/surveyresult.html', results)


# Django view to handle unknown paths
def unknown_path(request, random):
    return render(request, 'survey/unknownpath.html')
