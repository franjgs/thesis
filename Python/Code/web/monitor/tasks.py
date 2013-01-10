from celery import task
from tweepy import Stream
from dateutil import parser

from monitor import twitter
from monitor.models import Tweet

from web import settings

@task
def fetch_from_twitter():
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
