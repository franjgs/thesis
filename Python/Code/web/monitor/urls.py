from django.conf.urls import patterns, url

urlpatterns = patterns('monitor.views',
    (r'^$', 'index'),
    (r'^train/$', 'train'),
    (r'^fetch/$', 'fetch'),
    (r'^update_stats/$', 'update_stats'),
    (r'^(?P<name>\w+)/$', 'stats'),
)
