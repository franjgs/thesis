from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'web.views.index'),
    url(r'^ratings/', include('ratings.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
