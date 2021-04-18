from django.shortcuts import render
from django.http import HttpResponse,JsonResponse, HttpRequest, HttpResponseServerError, HttpResponseRedirect
from django import views

# Create your views here.

def start(request):
    '''
    Renders the main page for voting rules
    '''

    return render(request,'votingsim/main.html',{})