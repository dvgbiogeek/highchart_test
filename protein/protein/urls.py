from django.conf.urls import patterns, include, url
from django.contrib import admin
from composition.views import home, protein, thanks

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'composition.views.home', name='home'),
    url(r'^protein/$', 'composition.views.protein', name='protein'),
    url(r'^thanks/$', 'composition.views.thanks', name='thanks'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
