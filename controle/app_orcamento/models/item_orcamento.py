from django.db import models
from orcamento import Orcamento
from produto import Produto


class Item_Orcamento(models.Model):
    orcamento = models.ForeignKey(Orcamento)
    produto = models.ForeignKey(Produto)
    vl_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    vl_desconto = models.DecimalField(max_digits=10, decimal_places=2)
    observacao = models.CharField(max_length=250)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)

    def __eq__(self, other):
        return self.produto_id == other.produto_id

    class Meta:
        app_label = 'app_orcamento'