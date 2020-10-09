from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .story_gen import story_generator
from django.shortcuts import render
import json 

# Create your views here.
def randomsurvey(request):
    # grab the story here
    content = story_generator().get_story()
    # When creating a survey, the model for the survey should save all the information about the scenarios
    scenarios = []
    context = {
        'scenarios': scenarios
    }
    return render(request,'survey/takesurvey.html',context)

# stores everything into the Question model
def generatePoll(request):
    context = RequestContext(request)
    if request.method == 'POST':
        questionString = request.POST['questionTitle']
        questionDesc = request.POST['desc']

        question = Question(question_txt=questionString, question_desc=questionDesc)

        question.save()

    """
    OPRA Code
        return HttpResponseRedirect(reverse('polls:AddStep2', args=(question.id,)))
    return render(request,'polls/add_step1.html', {})
    """

    # eventually return something
    return(None)

# Start survey

# Collect user input from survey

# page for user survey creation <-- ??
    # get user defined rules back <-- ??

# Function to grab new scenario

def getsurvey(request):
    # grabbing the sample json
    sample = json.load(open('ethicssite/survey/sample.json','r'))

    print(sample)

    # For frontend, check the html to see how the object is grabbed.
    return render(request, 'survey/surveysample.html', context={"sample": sample})
    
    # once you navigate to http://127.0.0.1:8000/survey/getsurvey and press ctrl+shift+i and switch to console tab, 
    # you can see the json object printed on the console
    
