from django.db import models
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings


class Produto(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.CharField(max_length=250, null=True,blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)

    def __eq__(self, other):
        return self.id == other.id

    def get_page(self, page, busca):

        prods = Produto.objects.filter()

        if busca is not None:
            if '%' in busca:
                busca = busca.replace('%', '')
                prods = prods.filter(Q(nome__icontains=busca) | Q(descricao__icontains=busca))
            else:

                try:
                    id = int(busca)
                    prods = prods.filter(Q(id=id))
                except:
                    prods = prods.filter(Q(nome=busca))



        prods = prods.order_by('nome')
        paginator = Paginator(prods, settings.NR_REGISTROS_PAGINA)
        try:
            prods_page = paginator.page(page)
        except:
            prods_page = paginator.page(paginator.num_pages)

        return prods_page

    class Meta:
        app_label = 'app_orcamento'
