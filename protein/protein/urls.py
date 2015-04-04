from django.conf.urls import patterns, include, url
from django.views.static import serve
from django.contrib import admin
from account.views import user_login, new_user
from composition.views import home, protein, protein_detail, composition_detail
from glossary.views import terms, new
# from account.form import AuthenticateForm

from tastypie.api import Api
from api.protein_resource import ProteinResource
from api.glossary_resource import GlossaryResource

v1_api = Api(api_name='v1')
v1_api.register(ProteinResource())
v1_api.register(GlossaryResource())

urlpatterns = patterns('',
    # Home Page
    url(r'^$', 'composition.views.home', name='home'),
    # Protein Composition urls
    url(r'^protein/$', 'composition.views.protein', name='protein'),
    url(r'^protein/(\d+)/$', 'composition.views.protein_detail', name='protein_detail'),
    url(r'^protein/composition/(\d+)$', 'composition.views.composition_detail', name='composition_detail'),

    # Glossary
    url(r'^glossary/$', 'glossary.views.terms', name='terms'),
    url(r'^glossary/new/$', 'glossary.views.new', name='new'),

    # accounts
    url(r'^login/$', 'account.views.user_login', name='user_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {
            'template_name': 'home.html'}),
    url(r'^new_user/$', 'account.views.new_user', name='new_user'),
    # testing url
    url(r'^thanks$', 'composition.views.thanks', name='thanks'),
    # tastypie api for data
    url(r'^api/', include(v1_api.urls)),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # static_files
    # url(r'^static/(?P<path>.*)$', "django.views.static.serve', {'document_root: settings.STATICFILES_DIRS}"),
)
