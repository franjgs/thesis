from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext

from ratings.models import Story
from web import config

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
    return redirect("/ratings/")

def fetch(request):
    for name in ['depression', 'happy', 'suicidewatch']:
        reddit = praw.Reddit(user_agent = name + ' user agent')
        subreddit = reddit.get_subreddit(name)
        submissions = subreddit.get_hot(limit = config.STORIES)
        for x in submissions:
            if Story.objects.filter(id36 = x.id).count() == 0:
                story = Story(id36 = x.id, content = x.title, label = 0)
                story.save()
    return redirect("/ratings/")
