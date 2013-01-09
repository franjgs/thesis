from django.db import models

# 'id36' stores the reddit-allocated id of the story
# 'content' stores the story text
# 'subreddit' stores which subreddit was this story picked from
# 'label'
#       0 => not yet labelled
#       1 => depressed
#      -1 => happy
class Story(models.Model):

    id36        = models.CharField(max_length = 10, db_index = True)
    content     = models.CharField(max_length = 500)
    subreddit   = models.CharField(max_length = 50, blank = True)
    label       = models.IntegerField(default = 0)

    def __unicode__(self):
        return "%s (%s)" % (self.content, self.subreddit)
