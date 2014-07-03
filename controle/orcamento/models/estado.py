from django.db import models

class Estado(models.Model):
    abreviado = models.CharField(max_length=10,primary_key=True)
    nome = models.CharField(max_length=200)

    def __unicode__(self):
        return self.nome

    class Meta:
        app_label = 'orcamento'