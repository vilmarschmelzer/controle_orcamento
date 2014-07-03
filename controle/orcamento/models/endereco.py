from django.db import models
from cidade import Cidade

class Endereco(models.Model):
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=50)
    bairro = models.CharField(max_length=200)
    cep = models.BigIntegerField()
    referencia = models.CharField(max_length=200,null=True)
    cidade = models.ForeignKey(Cidade)

    class Meta:
        app_label = 'orcamento'