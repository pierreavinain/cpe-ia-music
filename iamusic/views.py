from django.http import HttpResponse
from django.shortcuts import render
from iamusic import gtzan_model, user_model

def home(request):
    gtzan = gtzan_model.GtzanModel()
    return render(request, 'index.html', {})
    # return HttpResponse("Hello World!")
