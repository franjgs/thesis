from django.conf.urls import patterns, url

urlpatterns = patterns('ratings.views',
    (r'^$', 'index'),
    (r'^/(?P<story_id>\d+)/rate/$', 'rate'),
    (r'^/fetch/$', 'fetch'),
)
