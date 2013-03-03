from django.db import connection
from django.shortcuts import render_to_response

from monitor.models import Stats

def index(request):
    cursor = connection.cursor()
    cursor.execute("select tweet_id, text, username, created_at from monitor_tweet order by (label_svm + label_bagging + label_boosting + label_stacking) desc limit 5")
    tweets = cursor.fetchall()
    cursor.close()
    return render_to_response("monitor/index.html", { 'tweets': tweets })

def stats(request, name):
    context = { 'name': name, 'data': Stats.for_model(name) }
    return render_to_response("monitor/index.html", context)
