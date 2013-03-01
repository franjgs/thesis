import praw
from celery import task
from ratings.models import Story
from web import settings

@task
def fetch_from_reddit():
    count = 0
    for name in settings.SUBREDDITS:
        reddit = praw.Reddit(user_agent = name + ' user agent')
        subreddit = reddit.get_subreddit(name)
        submissions = subreddit.get_hot(limit = settings.MAX_STORIES)
        for x in submissions:
            if Story.objects.filter(id36 = x.id).count() == 0:
                story = Story(
                    id36 = x.id,
                    content = x.title,
                    label = 0,
                    subreddit = name
                )
                story.save()
                count = count + 1
