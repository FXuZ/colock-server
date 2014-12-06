from django.conf.urls import patterns, include, url

from django.contrib import admin
import user_manage.views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'colock.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/', user_manage.views.register),
    url(r'^send/', message.views.send),
    url(r'^download/', message.views.download),
)

