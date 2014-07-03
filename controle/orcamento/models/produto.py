from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=250)
    descricao = models.CharField(max_length=250,null=True)
    valor = models.FloatField()

    class Meta:
        app_label = 'orcamento'
