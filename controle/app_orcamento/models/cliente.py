from endereco import Endereco
from django.db import models
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings


class Cliente(models.Model):
    documento = models.CharField(max_length=14, unique=True)
    nome = models.CharField(max_length=200)
    endereco = models.ForeignKey(Endereco)

    def get_page(self, page, busca):

        clientes = Cliente.objects.filter()

        if busca is not None:
            clientes = clientes.filter(Q(nome__icontains=busca) | Q(documento__icontains=busca))

        clientes = clientes.order_by('nome')

        paginator = Paginator(clientes, settings.NR_REGISTROS_PAGINA)
        try:
            clientes_page = paginator.page(page)
        except:
            clientes_page = paginator.page(paginator.num_pages)

        return clientes_page

    def get_contatos(self, id=None):
        from contato import Contato
        if id is None:
            id = self.id

        return Contato.objects.filter(cliente_id=id).all()

    class Meta:
        app_label = 'app_orcamento'