from django.db import models
from tipo_contato import Tipo_Contato
from cliente import Cliente


class Contato(models.Model):
    tipo_contato = models.ForeignKey(Tipo_Contato)
    cliente = models.ForeignKey(Cliente)
    contato = models.CharField(max_length=200)

    def __eq__(self, other):

        return self.id == other.id and self.tipo_contato == other.tipo_contato and \
               self.cliente_id == other.cliente_id and self.contato == other.contato

    class Meta:
        app_label = 'app_orcamento'