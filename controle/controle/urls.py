from django.conf.urls import patterns, include, url
from django.conf import settings
from app_orcamento.views import ProdutoView, ProdutoListView, ProdutoListAjaxView, ClienteListAjaxView, ClienteListView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'controle.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

    url(r'^cargainicial/$', 'app_orcamento.views.carga_inicial.carga', name='carga'),

    url(r'^logout/$', 'app_orcamento.views.controle.logout_user', name='logout_user'),

    url(r'^$', 'app_orcamento.views.controle.index', name='index'),
    url(r'^admin/add/usuario/$', 'app_orcamento.views.usuario.adicionar', name='adicionar'),
    url(r'^admin/editar/usuario/(?P<user_id>\d+)/$', 'app_orcamento.views.usuario.editar', name='editar'),
    url(r'^admin/consulta/usuarios/$', 'app_orcamento.views.usuario.consulta', name='consulta'),
    url(r'^perfil/$', 'app_orcamento.views.usuario.salvar_perfil', name='salvar_perfil'),

    url(r'^produto/salvar/$', ProdutoView.as_view(), name='salvar'),
    url(r'^produto/salvar/(?P<id>\d+)/$', ProdutoView.as_view(), name='salvar'),
    url(r'^produto/consultar/$', ProdutoListView.as_view(), name='consultar'),
    url(r'^produto/consulta_itens/$', ProdutoListAjaxView.as_view(), name='consulta_itens'),

    url(r'^cliente/salvar/$', 'app_orcamento.views.cliente.salvar', name='salvar'),
    url(r'^cliente/salvar/(?P<id>\d+)/$', 'app_orcamento.views.cliente.salvar', name='salvar'),
    url(r'^cliente/add_contato/$', 'app_orcamento.views.cliente.add_contato', name='add_contato'),
    url(r'^cliente/rm_contato/$', 'app_orcamento.views.cliente.rm_contato', name='rm_contato'),
    url(r'^cliente/consulta/$', ClienteListView.as_view(), name='consulta'),
    url(r'^cliente/consulta_itens/$', ClienteListAjaxView.as_view(), name='consulta_itens'),

    url(r'^orcamento/salvar/$', 'app_orcamento.views.orcamento.salvar', name='salvar'),
    url(r'^orcamento/salvar/(?P<id>\d+)/$', 'app_orcamento.views.orcamento.salvar', name='salvar'),
    url(r'^orcamento/add_produto/$', 'app_orcamento.views.orcamento.add_produto', name='add_produto'),
    url(r'^orcamento/rm_produto/$', 'app_orcamento.views.orcamento.rm_produto', name='rm_produto'),
    url(r'^orcamento/edit_produto/$', 'app_orcamento.views.orcamento.edit_produto', name='edit_produto'),
    url(r'^orcamento/consulta/$', 'app_orcamento.views.orcamento.consulta', name='consulta'),
    url(r'^orcamento/print/(?P<id>\d+)/$', 'app_orcamento.views.orcamento.print_orcamento', name='print_orcamento'),

    url(r'^cidade/get_cidades/$', 'app_orcamento.views.cidade.get_cidades', name='get_cidades'),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'controle/login.html'}),
)
