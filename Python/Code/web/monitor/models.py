from django.db import models
from django.utils.timezone import utc
import datetime

class Tweet(models.Model):
    
    tweet_id = models.BigIntegerField(default = 0, db_index = True)
    text = models.CharField(max_length = 500)
    created_at = models.DateTimeField(default = datetime.datetime.utcnow().replace(tzinfo = utc))
    username = models.CharField(max_length = 50)
    label = models.IntegerField(default = 0)
    
    def __unicode__(self):
        return "(%d) %s" % (self.tweet_id, self.text)

class Stats(models.Model):
    
    created_at = models.DateField(default = datetime.date.today(), db_index = True)
    depressed_count = models.IntegerField(default = 0)
    happy_count = models.IntegerField(default = 0)
    
    def __unicode__(self):
        return "%s: %d depressed and %d happy" % (str(self.created_at), self.depressed_count, self.happy_count)
