from django.db import connection
from django.shortcuts import render_to_response

from monitor.models import Tweet, Stats

def index(request):
    tweets = Tweet.objects.extra(
        select = { 'label_sum': 'label_svm + label_bagging + label_boosting + label_stacking' },
        order_by = ('-label_sum',)
    )[0:5]
    return render_to_response("monitor/index.html", { 'tweets': tweets })

def stats(request, name):
    context = {
        'name': name,
        'data': Stats.for_model(name),
        'labelled_tweets': Tweet.labelled_by_date(name)
    }
    return render_to_response("monitor/index.html", context)
