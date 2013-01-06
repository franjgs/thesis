from django.db import models
from django.utils.timezone import utc
import datetime

class Tweet(models.Model):
    
    tweet_id = models.BigIntegerField(default = 0, db_index = True)
    text = models.CharField(max_length = 500)
    created_at = models.DateTimeField(default = datetime.datetime.utcnow().replace(tzinfo = utc))
    username = models.CharField(max_length = 50)
    
    def __unicode__(self):
        return "(%d) %s" % (self.tweet_id, self.text)
