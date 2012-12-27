from django.db import models

# 'id36' stores the reddit-allocated id of the story
# 'content' stores the story text
# 'label' is 1 if the content is supposed to be depressed, -1 if it is happy, and 0 otherwise
class Story(models.Model):

    id36    = models.CharField(max_length = 10, db_index = True)
    content = models.CharField(max_length = 500)
    label   = models.IntegerField(default = 0)

    def __unicode__(self):
        return "%s (%s)" % (self.content, self.id36)
