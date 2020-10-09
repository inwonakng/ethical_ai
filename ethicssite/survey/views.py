from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .story_gen import story_generator
from django.shortcuts import render
import json

"""
    Create your views here.
"""


def random_survey(request):
    # grab the story here
    content = story_generator().get_story()
    # When creating a survey, the model for the survey
    # should save all the information about the scenarios
    scenarios = []
    context = {
        'scenarios': scenarios
    }
    return render(request, 'survey/takesurvey.html', context)

    # start survey
    # collect user input from survey
    # page for user survey creation
    # get user defined rules back
    # function to grab new scenario


def get_survey(request):
    # grabbing the sample json
    sample = json.load(open('survey/sample.json', 'r'))

    print(sample)

    # For frontend, check the html to
    # see how the object is grabbed.
    return render(request,
                  'survey/surveysample.html', context={"sample": sample})

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
