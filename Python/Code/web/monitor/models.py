from django.db import models
from django.utils.timezone import utc
import datetime

class Tweet(models.Model):
    
    tweet_id = models.BigIntegerField(default = 0, db_index = True)
    text = models.CharField(max_length = 500)
    created_at = models.DateTimeField(default = datetime.datetime.utcnow().replace(tzinfo = utc))
    username = models.CharField(max_length = 50)
    
    label_svm = models.IntegerField(default = 0)
    label_bagging = models.IntegerField(default = 0)
    label_boosting = models.IntegerField(default = 0)
    label_stacking = models.IntegerField(default = 0)
    
    def __unicode__(self):
        return "(%d) %s" % (self.tweet_id, self.text)
    
    @classmethod
    def from_today(cls):
        return cls.objects.filter(
            created_at__gte = datetime.datetime.combine(
                datetime.datetime.utcnow().date(),
                datetime.time()
            ).replace(tzinfo = utc)
        )
    
    @classmethod
    def unlabelled(cls):
        return cls.objects.filter(
            label_svm = 0,
            label_bagging = 0,
            label_boosting = 0,
            label_stacking = 0
        )

class Stats(models.Model):
    
    created_at = models.DateField(default = datetime.date.today(), db_index = True)
    
    depressed_count_svm = models.IntegerField(default = 0)
    depressed_count_bagging = models.IntegerField(default = 0)
    depressed_count_boosting = models.IntegerField(default = 0)
    depressed_count_stacking = models.IntegerField(default = 0)
    
    not_depressed_count_svm = models.IntegerField(default = 0)
    not_depressed_count_bagging = models.IntegerField(default = 0)
    not_depressed_count_boosting = models.IntegerField(default = 0)
    not_depressed_count_stacking = models.IntegerField(default = 0)
    
    def __unicode__(self):
        return "Stats for %s" % str(self.created_at)
    
    @classmethod
    def for_model(cls, name):
        return cls.objects.values(
            "created_at",
            "depressed_count_" + name,
            "not_depressed_count_" + name
        )
