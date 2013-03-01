from django.shortcuts import render_to_response

from monitor.models import Stats

def index(request):
    return render_to_response("monitor/index.html")

def stats(request, name):
    context = { 'name': name, 'data': Stats.for_model(name) }
    return render_to_response("monitor/index.html", context)
