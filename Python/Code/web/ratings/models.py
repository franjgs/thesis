from django.db import models

# 'content' stores the story text
# 'label' is 1 if the content is supposed to be depressed, -1 if it is happy, and 0 otherwise
class Story(models.Model):
    content = models.CharField(max_length = 500)
    label = models.IntegerField(default = 0)
    def __unicode__(self):
        return self.content
