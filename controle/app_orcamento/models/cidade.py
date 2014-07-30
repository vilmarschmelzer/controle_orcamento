from django.db import models
from estado import Estado


class Cidade(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=200)
    estado = models.ForeignKey(Estado)

    def __unicode__(self):
        return self.nome

    class Meta:
        app_label = 'app_orcamento'
