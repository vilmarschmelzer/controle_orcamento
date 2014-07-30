from django.db import models


class Tipo_Contato(models.Model):
    nome = models.CharField(max_length=100)
    mascara = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return self.nome

    class Meta:
        app_label = 'app_orcamento'