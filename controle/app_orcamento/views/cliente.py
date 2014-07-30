from django.shortcuts import render, RequestContext, HttpResponse
from app_orcamento.permissoes import group_required
from django.db import transaction
from django.conf import settings
from app_orcamento.forms.pesquisa import FormPesquisa
from app_orcamento.forms.cliente import FormCliente, FormContato
from app_orcamento.models import Cliente, Endereco, Tipo_Contato, Contato
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.utils import simplejson
from django.db.models import Q
from django.views.generic.base import View
from ajaxable_response_mixin import AjaxableResponseMixin
from django.utils.decorators import method_decorator


def __salvar(request, href, id=None):
    form = FormCliente(request.POST['estado'], id, request.POST)
    if form.is_valid() and len(request.session['contatos']) > 0:

        if id:
            cliente = Cliente.objects.get(pk=id)
            endereco = cliente.endereco
        else:
            cliente = Cliente()
            endereco = Endereco()

        cliente.nome = request.POST['nome']
        cliente.documento = form.get_documento()

        endereco.rua = request.POST['rua']
        endereco.numero = request.POST['numero']
        endereco.cidade_id = request.POST['cidade']
        endereco.bairro = request.POST['bairro']
        endereco.cep = request.POST['cep']
        endereco.referencia = request.POST['referencia']

        endereco.save()

        cliente.endereco_id = endereco.id
        cliente.save()

        contato_ids = []
        for contato in request.session['contatos']:
            contato.cliente_id = cliente.id
            contato.save()
            contato_ids.append(contato.id)

        Contato.objects.filter(~Q(id__in=contato_ids), Q(cliente_id = cliente.id)).delete()

        json = simplejson.dumps(
            {'success': True, 'href': href, 'id': cliente.id, 'nome': cliente.nome}, ensure_ascii=False)
        return HttpResponse(json, mimetype='application/json')

    html_contatos = ''
    if len(request.session['contatos']) == 0:
        html_contatos = render_to_string('msg_erro.html', {'msg': 'Adicione pelo menos um contato'},
                                         context_instance=RequestContext(request))

    html = render_to_string('cliente/fields_cliente.html', {'form': form}, context_instance=RequestContext(request))
    html = '<script src="%sjs/orcamento.js"></script>%s' % (settings.STATIC_URL, html)
    json = simplejson.dumps({'html': unicode(html), 'html_contatos': unicode(html_contatos), 'success': False},
                            ensure_ascii=False)

    return HttpResponse(json, mimetype='application/json')


@csrf_exempt
@transaction.commit_on_success
@group_required(settings.PERM_GRUPO_VENDEDOR)
def salvar(request, id=None):

    if request.method == 'POST':

        return __salvar(request, '/', id)

    else:
        contatos = []
        if id:
            cliente = Cliente.objects.get(pk=id)

            data = {'id': cliente.id,
                    'documento': cliente.documento,
                    'nome': cliente.nome,
                    'rua': cliente.endereco.rua,
                    'numero': cliente.endereco.numero,
                    'estado': cliente.endereco.cidade.estado_id,
                    'cidade': cliente.endereco.cidade_id,
                    'bairro': cliente.endereco.bairro,
                    'cep': cliente.endereco.cep,
                    'referencia': cliente.endereco.referencia
                    }
            form = FormCliente(cliente.endereco.cidade.estado_id, id, initial=data)

            request.session['index_contato'] = 0
            contatos = list(cliente.get_contatos())

            for contato in contatos:
                request.session['index_contato'] += 1
                contato.index_contato = request.session['index_contato']

            request.session['contatos'] = contatos

        else:
            form = FormCliente(None, None)

            request.session['contatos'] = []
            request.session['index_contato'] = 0
        formContato = FormContato()
    return render(request, 'cliente/cliente.html', {'form': form, 'formContato': formContato, 'contatos': contatos})


@csrf_exempt
def add_contato(request):

    if request.method == 'POST':
        contatos = request.session['contatos']
        form = FormContato(request.POST)

        if form.is_valid():

            contato = Contato()
            contato.tipo_contato = Tipo_Contato.objects.get(pk=request.POST['tipo_contato'])
            contato.contato = request.POST['contato']
            contato.index_contato = request.session['index_contato'] + 1

            contatos.append(contato)
            request.session['contatos'] = contatos
            request.session['index_contato'] += 1
            form = FormContato()

            formhtml = render_to_string('cliente/fields_contato.html', {'formContato': form})
        else:
            formhtml = render_to_string('cliente/fields_contato.html', {'formContato': form})

        contatoshtml = render_to_string('cliente/contatos.html', {'contatos': contatos})
        json = simplejson.dumps({'formhtml': unicode(formhtml), 'contatos': unicode(contatoshtml)}, ensure_ascii=False)
        return HttpResponse(json, mimetype='application/json')


@csrf_exempt
@group_required(settings.PERM_GRUPO_VENDEDOR)
def rm_contato(request):

    contatos = request.session['contatos']
    remover = None

    for contato in contatos:
        if contato.index_contato == int(request.POST['index_contato']):
            remover = contato
            break

    if remover is not None:
        contatos.remove(remover)

    request.session['contatos'] = contatos
    contatoshtml = render_to_string('cliente/contatos.html', {'contatos': contatos})
    json = simplejson.dumps({'contatos': unicode(contatoshtml)}, ensure_ascii=False)

    return HttpResponse(json, mimetype='application/json')


class ClienteListAjaxView(AjaxableResponseMixin, View):

    def __page(self, request):
        valor = None

        if request.method == 'POST':
            form = FormPesquisa(request.POST)
            if form.is_valid():
                valor = request.POST['valor']

        elif 'valor' in request.GET:
            valor = request.GET['valor']

        try:
            page = int(request.GET.get('page', 1))
        except Exception:
            page = 1

        clientes_page = Cliente().get_page(page, valor)

        clientes_html = render_to_string('cliente/itens_consulta.html', {'form': form, 'clientes': clientes_page})
        clientes_html ='<script src="%sjs/orcamento.js"></script>%s' % (settings.STATIC_URL, clientes_html)

        context = {'clientes': unicode(clientes_html)}

        return self.render_to_json_response(context)

    @method_decorator(group_required(settings.PERM_GRUPO_VENDEDOR))
    def get(self, request):
        return self.__page(request)

    @method_decorator(group_required(settings.PERM_GRUPO_VENDEDOR))
    def post(self, request):
        return self.__page(request)


class ClienteListView(View):
    form_class = FormPesquisa
    template_name = 'cliente/consulta.html'

    def __page(self, request):
        valor = None

        if request.method == 'POST':
            form = FormPesquisa(request.POST)

            if form.is_valid():
                valor = request.POST['valor']

        elif 'valor' in request.GET:
            valor = request.GET['valor']

        if valor is None or valor == 'None':
            form = self.form_class()
        else:
            data = {'valor': valor}

            form = self.form_class(initial=data)

        try:
            page = int(request.GET.get('page', 1))
        except:
            page = 1

        clientes_page = Cliente().get_page(page, valor)
        return render(request, self.template_name, {'form': form, 'clientes': clientes_page})

    @method_decorator(group_required(settings.PERM_GRUPO_VENDEDOR))
    def get(self, request):
        return self.__page(request)

    @method_decorator(group_required(settings.PERM_GRUPO_VENDEDOR))
    def post(self, request):
        return self.__page(request)