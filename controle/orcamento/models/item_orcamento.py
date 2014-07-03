from django.db import models
from orcamento import Orcamento
from produto import Produto

class Item_Orcamento(models.Model):
    orcamento = models.ForeignKey(Orcamento)
    produto = models.ForeignKey(Produto)
    vl_unitario = models.FloatField()
    vl_desconto = models.FloatField()
    observacao = models.CharField(max_length=250)
    quantidade = models.FloatField()

    class Meta:
        app_label = 'orcamento'