from django.db import models


class Estado(models.Model):
    id = models.IntegerField(primary_key=True)
    abreviado = models.CharField(max_length=3)
    nome = models.CharField(max_length=200)

    def __unicode__(self):
        return self.nome

    class Meta:
        app_label = 'app_orcamento'