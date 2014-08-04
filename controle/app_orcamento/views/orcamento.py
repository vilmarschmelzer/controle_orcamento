# coding:utf-8
from django.shortcuts import render, HttpResponse, RequestContext
from app_orcamento.permissoes import group_required
from django.db import transaction
from django.conf import settings
from app_orcamento.forms.pesquisa import FormPesquisa
from app_orcamento.forms.orcamento import FormOrcamento, FormItem
from app_orcamento.models import Produto, Orcamento, ItemOrcamento, Cliente
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.utils import simplejson
from django.db.models import Q
from datetime import datetime
from django.template import loader
from report import process_latex


@csrf_exempt
@transaction.commit_on_success
@group_required(settings.PERM_GRUPO_VENDEDOR)
def salvar(request, id=None):

    if request.method == 'POST':
        form = FormOrcamento(request.POST)
        itens = request.session['itens_orcamento']
        if form.is_valid() and len(itens) > 0:
            if id:
                orcamento = Orcamento.objects.get(pk=id)
            else:
                orcamento = Orcamento()

            orcamento.dt_criacao = datetime.today()
            orcamento.usuario_id = request.user.id

            id_cliente = Cliente.objects.filter(documento=request.POST['cliente'].split(' - ')[0]).get().id
            orcamento.cliente_id = id_cliente
            orcamento.observacao = request.POST['observacao']

            aprovado = None

            if form.cleaned_data['aprovado'] == 1:
                aprovado = True
            elif form.cleaned_data['aprovado'] == 0:
                aprovado = False

            orcamento.aprovado = aprovado
            orcamento.nr_dias_validade = request.POST['nr_dias_validade']

            orcamento.save()

            itens_ids = []
            for item in request.session['itens_orcamento']:
                item.orcamento_id = orcamento.id
                item.vl_unitario = item.produto.valor
                item.save()
                itens_ids.append(item.id)

            ItemOrcamento.objects.filter(Q(orcamento_id=orcamento.id), ~Q(id__in=itens_ids)).delete()

            json = simplejson.dumps({'success': True, 'href': '/'}, ensure_ascii=False)
            return HttpResponse(json, mimetype='application/json')

        html_produtos = ''
        if len(itens) == 0:
            html_produtos = render_to_string('msg_erro.html', {'msg': 'Adicione pelo menos um produto'},
                                         context_instance=RequestContext(request))

        html = render_to_string('orcamento/fields_orcamento.html', {'form': form},
                                context_instance=RequestContext(request))
        html = '<script src="%sjs/orcamento.js"></script>%s' % (settings.STATIC_URL, html)
        json = simplejson.dumps({'html': unicode(html), 'html_produtos': unicode(html_produtos), 'success': False},
                            ensure_ascii=False)

        return HttpResponse(json, mimetype='application/json')

    else:
        formItem = FormItem()
        if id:
            orcamento = Orcamento.objects.get(pk=id)
            data = {'id': id,
                    'cliente': ('%s - %s' % (orcamento.cliente.documento, orcamento.cliente.nome)),
                    'observacao': orcamento.observacao,
                    'nr_dias_validade': orcamento.nr_dias_validade,
                    'aprovado': orcamento.aprovado}
            form = FormOrcamento(initial=data)
            request.session['itens_orcamento'] = orcamento.get_itens()

            return render(request, 'orcamento/orcamento.html', {'form': form, 'formItem': formItem, 'id': id,
                                                                'formPesquisa': FormPesquisa(), 'orcamento': orcamento})
        else:
            request.session['itens_orcamento'] = []
            form = FormOrcamento()

    return render(request, 'orcamento/orcamento.html', {'form': form, 'formItem': formItem, 'id': id,
                                                        'formPesquisa': FormPesquisa()})


@csrf_exempt
def add_produto(request):
    itens = request.session['itens_orcamento']
    if request.method == 'POST':

        form = FormItem(request.POST)

        if form.is_valid():

            #produto id get pelo form
            id = int(request.POST['produto'].split(' - ')[0])
            _item = None

            for item in itens:
                if item.produto.id == id:
                    print 'encontro'
                    _item = item

                    break

            if _item is None:
                _item = ItemOrcamento()
                _item.produto = Produto.objects.get(pk=id)
            else:
                itens.remove(_item)

            _item.quantidade = request.POST['quantidade']
            if request.POST['vl_desconto']:
                _item.vl_desconto = request.POST['vl_desconto']
            else:
                _item.vl_desconto = 0
            _item.observacao = request.POST['observacao']

            itens.append(_item)
            request.session['itens_orcamento'] = itens

            form = FormItem()

            formhtml = render_to_string('orcamento/fields_produto.html', {'formItem': form})
        else:
            formhtml = render_to_string('orcamento/fields_produto.html', {'formItem': form})

        orcamento = Orcamento()
        orcamento.set_itens(itens)
        print 'itens : ', orcamento.get_total_produtos()

        produtoshtml = render_to_string('orcamento/produtos.html', {'orcamento': orcamento})
        json = simplejson.dumps({'formhtml': unicode(formhtml), 'produtos': unicode(produtoshtml)}, ensure_ascii=False)
        return HttpResponse(json, mimetype='application/json')


@csrf_exempt
def edit_produto(request):

    if request.method == 'POST':
        itens = request.session['itens_orcamento']
        item_edit = None
        for item in itens:
            if item.produto.id == int(request.POST['produto_id']):
                item_edit = item
                break

        if item_edit is not None:
            data = {'produto': '%s - %s' % (item_edit.produto.id, item_edit.produto.nome),
                    'valor': item_edit.produto.valor,
                    'quantidade': item_edit.quantidade,
                    'vl_desconto': item_edit.vl_desconto,
                    'observacao': item_edit.observacao}
            form = FormItem(initial=data)
        else:
            form = FormItem()

        formhtml = render_to_string('orcamento/fields_produto.html', {'formItem': form})

        json = simplejson.dumps({'formhtml': unicode(formhtml)}, ensure_ascii=False)
        return HttpResponse(json, mimetype='application/json')


@csrf_exempt
def rm_produto(request):

    itens = request.session['itens_orcamento']
    remover = None

    for item in itens:
        if item.produto.id == int(request.POST['produto_id']):
            remover = item
            break

    if remover is not None:
        itens.remove(remover)

    request.session['itens_orcamento'] = itens
    orcamento = Orcamento()
    orcamento.set_itens(itens)

    produtoshtml = render_to_string('orcamento/produtos.html', {'orcamento': orcamento})
    json = simplejson.dumps({'produtos': unicode(produtoshtml)}, ensure_ascii=False)
    return HttpResponse(json, mimetype='application/json')


@group_required(settings.PERM_GRUPO_ADMINISTRADOR, settings.PERM_GRUPO_VENDEDOR)
def consulta(request):

    valor = None

    if request.method == 'POST':
        form = FormPesquisa(request.POST)

        if form.is_valid():
            valor = request.POST['valor']

    elif 'valor' in request.GET:
        valor = request.GET['valor']

    if valor is None or valor == 'None':
        form = FormPesquisa()
    else:
        data = {'valor': valor}
        form = FormPesquisa(initial=data)

    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1

    orcamentos_page = Orcamento().get_page(page, valor)

    return render(request, 'orcamento/consulta.html', {'form': form, 'orcamentos': orcamentos_page})


@group_required(settings.PERM_GRUPO_VENDEDOR)
def print_orcamento(request, id):
    orcamento = Orcamento.objects.get(pk=id)

    c = RequestContext(request, {'orcamento': orcamento})
    t = loader.get_template('orcamento/print.tex')
    latex = t.render(c)
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=orçamento-%s.pdf' % orcamento.id
    process_latex(latex, outfile=response)

    # abre o pdf na propria aba
    # return HttpResponse(response, mimetype='application/pdf')
    # baixar o arquivo direto
    return response
