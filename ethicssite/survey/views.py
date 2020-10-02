from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
# from .story_gen import make_story
from .models import DummyModel
from django.shortcuts import render

# Create your views here.
def randomsurvey(request):
    # grab the story here
    content = make_story()

    scenarios = [DummyModel.create(c) for c in content]
    # When creating a survey, the model for the survey should save all the information about the scenarios
    
    context = {
        'scenarios': scenarios
    }
    return render(request,'survey/takesurvey.html',context)