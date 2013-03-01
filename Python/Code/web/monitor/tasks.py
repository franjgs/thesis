from django.db import connection
from celery import task
from tweepy import Stream
from dateutil import parser

from monitor import twitter
from monitor.models import Tweet, Stats

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

def get_name(klass):
    return klass.__name__.lower()

@task
def update_statistic():
    """update distress stats about tweets"""
    print "update_statistics => BEGIN"
    # collect all the unique dates
    cursor = connection.cursor()
    cursor.execute("select distinct(date(created_at)) from monitor_tweet")
    dates = map(lambda x: x[0], cursor.fetchall())
    # iterate over dates and store labels
    for date in dates:
        # collect all the tweets for the particular date
        tweets = list()
        for tweet in Tweet.objects.filter(created_at__year = date.year, created_at__month = date.month, created_at__day = date.day):
            tweets.append(tweet)
        # store labels for tweets on this particular date
        print "update_statistics => Updating stats for " + str(date)
        try:
            stats = Stats.objects.get(created_at = date)
        except:
            stats = Stats()
        finally:
            for klass in [SVM, Bagging, Boosting, Stacking]:
                depressed_count, not_depressed_count = fetch_labels(klass, tweets)
                setattr(stats, "depressed_count_" + get_name(klass), depressed)
                setattr(stats, "not_depressed_count_" + get_name(klass), not_depressed)
            stats.save()
    print "update_statistics => DONE"
