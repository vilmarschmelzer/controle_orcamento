from django.db import models
from endereco import Endereco
from cliente import Cliente
from django.contrib.auth.models import User

class Orcamento(models.Model):
    dt_criacao = models.DateTimeField()
    cliente = models.ForeignKey(Cliente)
    observacao = models.CharField(max_length=250,null=True)
    aprovato = models.NullBooleanField()
    nr_dias_validade = models.IntegerField()
    endereco = models.ForeignKey(Endereco,null=True)
    usuario = models.ForeignKey(User)

    class Meta:
        app_label = 'orcamento'