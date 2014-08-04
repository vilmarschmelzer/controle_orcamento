from django.db import models
from tipo_contato import TipoContato
from cliente import Cliente


class Contato(models.Model):
    tipo_contato = models.ForeignKey(TipoContato)
    cliente = models.ForeignKey(Cliente)
    contato = models.CharField(max_length=200)

    def __eq__(self, other):

        return self.id == other.id and self.tipo_contato == other.tipo_contato and \
               self.cliente_id == other.cliente_id and self.contato == other.contato

    class Meta:
        app_label = 'app_orcamento'