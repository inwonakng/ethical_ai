from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .generation.Generator import Generator
from django.shortcuts import render
import json

def get_survey(request):
    # grab the story here
    # content = story_generator().get_story()
    # When creating a survey, the model for the survey
    # should save all the information about the scenarios
    scenarios = []
    context = {
        'scenarios': scenarios
    }
    return render(request, 'survey/takesurvey.html', context)

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
    # grabbing the sample json
    rule = json.load(open('ethicssite/survey/generation/rule/rule.json','r'))
    story_gen = Generator(rule=rule)
    ss = story_gen.get_scenario()
    print(ss)
    sample = json.dumps(ss)
    sample = json.dumps({'a':1,'b':2})

    # print(sample)

    # For frontend, check the html to
    # see how the object is grabbed.
    return render(request,
                  'survey/surveysample.html', context={"survey_information": survey_information})

    # once you navigate to http://127.0.0.1:8000/survey/getsurvey
    # and press ctrl+shift+i and switch to console tab,
    # you can see the json object printed on the console

# Django view to handle the survey results page.
def survey_result(request):
    results = {}
    return render(request, 'survey/surveyresult.html', results)


# Django view to handle unknown paths
def unknown_path(request, random):
    return render(request, 'survey/unknownpath.html')
