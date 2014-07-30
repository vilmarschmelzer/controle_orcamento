from django.shortcuts import render
from app_orcamento.permissoes import group_required
from django.conf import settings
from app_orcamento.forms.pesquisa import FormPesquisa
from app_orcamento.forms.produto import FormProduto
from app_orcamento.models.produto import Produto
from django.views.generic.base import View
from ajaxable_response_mixin import AjaxableResponseMixin
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string


class ProdutoView(View):
    form_class = FormProduto
    template_name = 'produto/produto.html'

    @method_decorator(group_required(settings.PERM_GRUPO_ADMINISTRADOR))
    def get(self, request, id=None):

        form = self.form_class(id)
        return render(request, self.template_name, {'form': form})

    @method_decorator(group_required(settings.PERM_GRUPO_ADMINISTRADOR))
    def post(self, request, id=None):

        form = self.form_class(id, request.POST)
        form.id = id
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')

        return render(request, self.template_name, {'form': form})


class ProdutoListAjaxView(AjaxableResponseMixin, View):
    form_class = FormPesquisa
    template_name = 'produto/itens_consulta.html'

    def __page(self, request):
        valor = None

        form = self.form_class(request.POST)
        if form.is_valid():
            valor = request.POST['valor']

        elif 'valor' in request.GET:
            valor = request.GET['valor']

        try:
            page = int(request.GET.get('page', 1))
        except Exception:
            page = 1

        produtos_page = Produto().get_page(page, valor)
        produtos_html = render_to_string(self.template_name, {'form': form, 'produtos': produtos_page})
        produtos_html ='<script src="%sjs/orcamento.js"></script>%s' % (settings.STATIC_URL, produtos_html)

        context = {'produtos': unicode(produtos_html)}
        js = self.render_to_json_response(context)
        return js

    def get(self, request):
        return self.__page(request)

    def post(self, request):
        return self.__page(request)


class ProdutoListView(View):
    form_class = FormPesquisa
    template_name = 'produto/consulta.html'

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

        prods_page = Produto().get_page(page, valor)
        return render(request, self.template_name, {'form': form, 'prods': prods_page})

    def get(self, request):
        return self.__page(request)

    def post(self, request):
        return self.__page(request)
