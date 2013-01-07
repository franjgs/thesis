from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages
from tweepy import Stream
from dateutil import parser

from monitor.classifiers.static import models
from monitor import twitter
from monitor.models import Tweet
from ratings.models import Story
from web import settings

def index(request):
    return render_to_response("monitor/index.html", context_instance = RequestContext(request))

def stats(request, name):
    context = None
    if name == "svm":
        context = { 'name': 'SVM' }
    else:
        context = { 'name': name.capitalize() }
    return render_to_response("monitor/index.html", context)

def train(request):
    labels, stories = list(), list()
    for story in Story.objects.exclude(label = 0):
        labels.append(int(story.label))
        stories.append(story.content)
    for model in models:
        clf = None
        if model.__name__ == "SVM":
            clf = model()
        else:
            clf = model(n_models = settings.N_MODELS)
        clf.fit(stories, labels)
        settings.CLASSIFIERS[model.__name__.lower()] = clf
    messages.add_message(request, messages.INFO, "Models trained on " + str(len(labels)) + " samples")
    return redirect("/monitor/")

def fetch(request):
    auth = twitter.get_auth()
    listener = twitter.Listener(settings.MAX_TWEETS)
    stream = Stream(auth, listener)
    stream.sample()
    for data in listener.buffer:
        if Tweet.objects.filter(tweet_id = data['id']).count() == 0:
            tweet = Tweet(
                tweet_id = data['id'],
                text = data['text'],
                created_at = parser.parse(data['created_at']),
                username = data['user']['screen_name']
            )
            tweet.save()
    messages.add_message(request, messages.INFO, "Fetched " + str(len(listener.buffer)) + " tweets from Twitter")
    return redirect("/monitor/")

def update_stats(request):
    # TODO
    messages.add_message(request, messages.INFO, "Updated statistics")
    return redirect("/monitor/")
