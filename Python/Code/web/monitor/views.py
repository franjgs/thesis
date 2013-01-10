from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages
import datetime

from monitor.classifiers.static import Classifiers
from monitor.models import Tweet, Stats
from monitor import tasks
from ratings.models import Story
from web import settings

def index(request):
    return render_to_response("monitor/index.html", context_instance = RequestContext(request))

def stats(request, name):
    context = dict()
    if name in Classifiers.__keys__:
        if Classifiers.trained(name):
            context['data'] = Stats.for_model(name)
            if name == "svm":
                context['name'] = "SVM"
            else:
                context['name'] = name.capitalize()
        else:
            context['data'] = None
            messages.add_message(request, messages.ERROR, "Classifier " + name + " not trained yet")
    else:
        context['data'] = None
        messages.add_message(request, messages.ERROR, "No classifier called " + name)
    return render_to_response("monitor/index.html", context_instance = RequestContext(request))

def train(request):
    if Story.objects.count() == 0:
        messages.add_message(request, messages.ERROR, "No samples in the database yet - please fetch some stories first")
    elif Story.objects.exclude(label = 0).count() == 0:
        messages.add_message(request, messages.ERROR, "No samples have been labelled yet - please label some stories first")
    else:
        labels, stories = list(), list()
        for story in Story.objects.exclude(label = 0):
            labels.append(int(story.label))
            stories.append(story.content)
        Classifiers.fit("all", stories, labels)
        messages.add_message(request, messages.INFO, "Trained models on " + str(len(labels)) + " samples")
    return redirect("/monitor/")

def fetch(request):
    tasks.fetch_from_twitter.delay()
    messages.add_message(request, messages.INFO, "Fetching " + str(settings.MAX_TWEETS) + " tweets from Twitter")
    return redirect("/monitor/")

def update_stats(request):
    if Classifiers.trained("all"):
        # fetch all the unlabelled tweets
        if Tweet.unlabelled().count() > 0:
            tweets = Tweet.unlabelled()
            # initialize all the labels variables
            labels = dict()
            for key in Classifiers.__keys__:
                labels[key] = None
            # get predictions from all the classifiers
            for clf in Classifiers.all():
                predicted = map(
                    lambda x: int(x),
                    clf.predict(
                        map(
                            lambda x: x.text,
                            tweets
                        )
                    )
                )
                labels[clf.get_name()] = predicted
            # save all the tweets with the newly assigned labels
            index = 0
            for tweet in tweets:
                for key in Classifiers.__keys__:
                    setattr(tweet, "label_" + key, labels[key][index])
                tweet.save()
                index = index + 1
            # add to statistics
            try:
                stats = Stats.objects.get(created_at = datetime.date.today())
            except:
                stats = Stats()
                stats.created_at = datetime.date.today()
                for key in Classifiers.__keys__:
                    depressed = labels[key].count(1)
                    not_depressed = labels[key].count(-1)
                    setattr(stats, "depressed_count_" + key, depressed)
                    setattr(stats, "not_depressed_count_" + key, depressed)
                stats.save()
            messages.add_message(request, messages.SUCCESS, "Updated statistics")
        else:
            messages.add_message(request, messages.INFO, "No unlabelled tweets left")
    else:
        messages.add_message(request, messages.ERROR, "Models not trained yet - please train them first")
    return redirect("/monitor/")
