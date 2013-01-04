from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):
    return render_to_response("monitor/index.html", {})

def stats(request, name):
    context = None
    if name == "svm":
        context = { 'name': 'SVM' }
    else:
        context = { 'name': name.capitalize() }
    return render_to_response("monitor/index.html", context)
