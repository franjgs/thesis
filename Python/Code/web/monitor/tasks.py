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

@task
def update_statistics():
    """update distress stats about tweets"""
    print "update_statistics => BEGIN"
    # collect the training data
    print "update_statistics => collecting training data"
    labels, stories = list(), list()
    for story in Story.objects.exclude(label = 0):
        labels.append(int(story.label))
        stories.append(story.content)
    # train the models
    print "update_statistics => training the classifiers on %d stories" % len(stories)
    clf = dict()
    for klass in [SVM, Bagging, Boosting, Stacking]:
        if klass == SVM:
            clf[klass] = klass()
        else:
            clf[klass] = klass(n_models = settings.N_MODELS)
        print "update_statistics => initializing %s" % klass.__name__
        clf[klass].fit(stories, labels)
    # collect all the unique dates
    print "update_statistics => collecting unique dates"
    cursor = connection.cursor()
    cursor.execute("select distinct(date(created_at)) from monitor_tweet")
    dates = map(lambda x: x[0], cursor.fetchall())
    print "update_statistics => collected %d unique dates" % len(dates)
    # iterate over dates and store labels
    for date in dates:
        # collect all the tweets for the particular date
        tweets = Tweet.objects.filter(
            created_at__year = date.year,
            created_at__month = date.month,
            created_at__day = date.day
        )
        tweets_text = map(lambda tweet: tweet.text, tweets)
        # store labels for tweets on this particular date
        print "update_statistics => Updating statistics for %s (%d tweets)" % (str(date), len(tweets))
        try:
            stats = Stats.objects.get(created_at = date)
        except:
            stats = Stats()
            stats.created_at = date
        finally:
            for klass in [SVM, Bagging, Boosting, Stacking]:
                plabels = map(lambda x: int(x), clf[klass].predict(tweets_text).tolist())
                # update overall statistics
                depressed_count = len([i for i in plabels if i == 1])
                not_depressed_count = len([i for i in plabels if i == -1])
                setattr(stats, "depressed_count_" + klass.__name__.lower(), depressed_count)
                setattr(stats, "not_depressed_count_" + klass.__name__.lower(), not_depressed_count)
                # update label of each tweet
                for i in xrange(0, len(plabels)):
                    setattr(tweets[i], "label_" + klass.__name__.lower(), plabels[i])
            # write overall statistics back to the database
            stats.save()
            # write label of each tweet back to the database
            for tweet in tweets:
                tweet.save()
    print "update_statistics => DONE"
