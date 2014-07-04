from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'controle.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

    url(r'^cargainicial/$', 'orcamento.views.carga_inicial.carga', name='carga'),

    url(r'^logout/$', 'orcamento.views.controle.logout_user', name='logout_user'),

    url(r'^$', 'orcamento.views.controle.index', name='index'),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'controle/login.html'}),
    url(r'^admin/', include(admin.site.urls)),
)
