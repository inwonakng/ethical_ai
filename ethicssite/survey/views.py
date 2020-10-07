from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .story_gen import story_generator
# from .models import DummyModel
from django.shortcuts import render

# Create your views here.
def randomsurvey(request):
    # grab the story here
    content = story_generator().get_story()

    scenarios = [DummyModel.create(c) for c in content]
    # When creating a survey, the model for the survey should save all the information about the scenarios
    
    context = {
        'scenarios': scenarios
    }
    return render(request,'survey/takesurvey.html',context)

    # start survey

    # collect user input from survey

    # page for user survey creation
        # get user defined rules back
    
    # function to grab new scenario