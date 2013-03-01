from django.db import connection
from celery import task
from tweepy import Stream
from dateutil import parser

from monitor import twitter
from monitor.models import Tweet, Stats
from ratings.models import Story

from monitor.classifiers.static.svm import SVM
from monitor.classifiers.static.bagging import Bagging
from monitor.classifiers.static.boosting import Boosting
from monitor.classifiers.static.stacking import Stacking

from web import settings

@task
def fetch_from_twitter():
    """fetch tweets from twitter"""
    print "fetch_from_twitter => BEGIN"
    auth = twitter.get_auth()
    listener = twitter.Listener(settings.MAX_TWEETS)
    stream = Stream(auth, listener)
    stream.sample()
    print "fetch_from_twitter => SAMPLED"
    for data in listener.buffer:
        if Tweet.objects.filter(tweet_id = data['id']).count() == 0:
            tweet = Tweet(
                tweet_id = data['id'],
                text = data['text'],
                created_at = parser.parse(data['created_at']),
                username = data['user']['screen_name']
            )
            try:
                tweet.save()
            except Exception, e:
                print "Error saving tweet " + str(tweet) + "(" + e.message + ")"
    stream.disconnect()
    print "fetch_from_twitter => DONE"

def fetch_labels(klass, tweets, stories, labels):
    if klass == SVM:
        clf = klass()
    else:
        clf = klass(n_models = settings.N_MODELS)
    clf.fit(stories, labels)
    plabels = map(lambda x: int(x), clf.predict(tweets).tolist())
    positive = len([i for i in plabels if i == 1])
    negative = len([i for i in plabels if i == -1])
    return (positive, negative)

@task
def update_statistics():
    """update distress stats about tweets"""
    print "update_statistics => BEGIN"
    # collect the training data
    labels, stories = list(), list()
    for story in Story.objects.exclude(label = 0):
        labels.append(int(story.label))
        stories.append(story.content)
    # collect all the unique dates
    cursor = connection.cursor()
    cursor.execute("select distinct(date(created_at)) from monitor_tweet")
    dates = map(lambda x: x[0], cursor.fetchall())
    # iterate over dates and store labels
    for date in dates:
        # collect all the tweets for the particular date
        tweets = Tweet.objects.filter(
            created_at__year = date.year,
            created_at__month = date.month,
            created_at__day = date.day
        ).values_list("text", flat = True)
        # store labels for tweets on this particular date
        print "update_statistics => Updating statistics for " + str(date)
        try:
            stats = Stats.objects.get(created_at = date)
        except:
            stats = Stats()
            stats.created_at = date
        finally:
            for klass in [SVM, Bagging, Boosting, Stacking]:
                depressed_count, not_depressed_count = fetch_labels(klass, tweets, stories, labels)
                setattr(stats, "depressed_count_" + klass.__name__.lower(), depressed_count)
                setattr(stats, "not_depressed_count_" + klass.__name__.lower(), not_depressed_count)
            stats.save()
    print "update_statistics => DONE"
