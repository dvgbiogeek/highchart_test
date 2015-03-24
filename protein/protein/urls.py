from django.conf.urls import patterns, include, url
from django.contrib import admin
from composition.views import home, protein, protein_detail, composition_detail

from tastypie.api import Api
from api.protein_resource import ProteinResource

v1_api = Api(api_name='v1')
v1_api.register(ProteinResource())

urlpatterns = patterns('',
    # Home Page
    url(r'^$', 'composition.views.home', name='home'),
    # Protein Composition urls
    url(r'^protein/$', 'composition.views.protein', name='protein'),
    url(r'^protein/(\d+)/$', 'composition.views.protein_detail', name='protein_detail'),
    url(r'^composition/(\d+)$', 'composition.views.composition_detail', name='composition_detail'),

    # tastypie api for data
    url(r'^api/', include(v1_api.urls)),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
