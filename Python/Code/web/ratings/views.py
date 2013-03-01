from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages

from ratings.models import Story
from ratings import tasks
from web import settings

import praw

def index(request):
    try:
        story = Story.objects.filter(label = 0)[0]
    except:
        return render_to_response(
            "ratings/index.html",
            { 'error_message': 'No unlabeled stories left' },
            context_instance = RequestContext(request)
        )
    return render_to_response(
        "ratings/index.html",
        { 'story': story },
        context_instance = RequestContext(request)
    )

def rate(request, story_id):
    story = get_object_or_404(Story, pk = story_id)
    if request.POST[u'label']:
        if request.POST[u'label'] == u'depressed':
            story.label = 1
        elif request.POST[u'label'] == u'happy':
            story.label = -1
        story.save()
    messages.add_message(request, messages.SUCCESS, "Stored")
    return redirect("/ratings/")
