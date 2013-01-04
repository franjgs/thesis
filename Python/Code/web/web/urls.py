from django.conf.urls import patterns, include, url
from web import settings

# Initialize django admin
from django.contrib import admin
admin.autodiscover()

# Initialize all the machine learning models
from monitor import startup
startup.initialize()

urlpatterns = patterns('',
    url(r'^$', 'web.views.index'),
    url(r'^ratings/', include('ratings.urls')),
    url(r'^monitor/', include('monitor.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
)
