from django.db import models
from endereco import Endereco
from cliente import Cliente
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings
from decimal import Decimal

TWOPLACES = Decimal(10) ** -2


class Orcamento(models.Model):
    dt_criacao = models.DateTimeField()
    cliente = models.ForeignKey(Cliente)
    observacao = models.CharField(max_length=250, null=True)
    aprovado = models.NullBooleanField()
    nr_dias_validade = models.IntegerField()
    usuario = models.ForeignKey(User)

    def set_itens(self, itens):
        self.itens = itens

    def get_itens(self):
        from item_orcamento import Item_Orcamento
        if not hasattr(self, 'itens'):
            if self.id == 0:
                self.itens = []
            else:
                self.itens = list(Item_Orcamento.objects.filter(orcamento_id=self.id).all())

        return self.itens

    def get_total_produtos(self):
        total = Decimal(0.0)
        for item in self.get_itens():

            total += Decimal(Decimal(item.produto.valor) * Decimal(item.quantidade)).quantize(TWOPLACES)

        return total

    def get_total_desconto(self):
        total = Decimal(0.0)

        for item in self.get_itens():
            if item.vl_desconto:
                total += Decimal(item.vl_desconto).quantize(TWOPLACES)

        return total

    def get_total(self):
        return self.get_total_produtos() - self.get_total_desconto()

    def get_page(self, page, busca):

        orcamentos = Orcamento.objects.filter()

        if busca is not None:
            orcamentos = orcamentos.filter(Q(cliente__nome__icontains=busca) | Q(cliente__documento__icontains=busca))

        orcamentos = orcamentos.order_by('id')
        paginator = Paginator(orcamentos, settings.NR_REGISTROS_PAGINA)
        try:
            orcamentos_page = paginator.page(page)
        except:
            orcamentos_page = paginator.page(paginator.num_pages)

        return orcamentos_page

    class Meta:
        app_label = 'app_orcamento'