from django.conf.urls import patterns, url

urlpatterns = patterns('monitor.views',
    (r'^$', 'index'),
    (r'^train/$', 'train'),
    (r'^(?P<name>\w+)/$', 'stats'),
)
